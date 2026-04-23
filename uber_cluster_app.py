import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import plotly.express as px


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))
    return R * c


@st.cache_data
def load_data_from_path(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    df = df.loc[:, ~df.columns.str.match('^Unnamed')]
    df.columns = [c.strip() for c in df.columns]
    for col in ["pickup_latitude", "pickup_longitude", "dropoff_latitude", "dropoff_longitude"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "pickup_datetime" in df.columns:
        df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], errors="coerce")
    if {"pickup_latitude", "pickup_longitude", "dropoff_latitude", "dropoff_longitude"}.issubset(df.columns):
        df["distance_km"] = haversine_km(df["pickup_latitude"], df["pickup_longitude"], df["dropoff_latitude"], df["dropoff_longitude"])
    else:
        for alt in ["distance", "trip_distance", "Distance"]:
            if alt in df.columns:
                df["distance_km"] = pd.to_numeric(df[alt], errors="coerce")
                break
    if "fare_amount" in df.columns:
        df["fare"] = pd.to_numeric(df["fare_amount"], errors="coerce")
    elif "Fare" in df.columns:
        df["fare"] = pd.to_numeric(df["Fare"], errors="coerce")
    else:
        numeric = df.select_dtypes("number")
        if not numeric.empty:
            df["fare"] = numeric.iloc[:, 0]
        else:
            df["fare"] = pd.NA
    df = df.loc[df["fare"].notna() & df["distance_km"].notna()].copy()
    df.reset_index(drop=True, inplace=True)
    return df


@st.cache_data
def run_clustering(df: pd.DataFrame, n_clusters: int, scale: bool = True):
    X = df[["fare", "distance_km"]].to_numpy()
    scaler = None
    if scale:
        scaler = StandardScaler()
        Xs = scaler.fit_transform(X)
    else:
        Xs = X
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(Xs)
    return labels, kmeans, scaler


def app():
    st.set_page_config(page_title="Uber fares explorer", layout="wide")

    st.title("Uber fares clustering explorer")

    with st.sidebar:
        st.header("Data input")
        upload = st.file_uploader("Upload CSV (optional)", type=["csv"])
        csv_path = st.text_input("Or CSV path (local)", value="uber.csv")
        st.markdown("---")
        st.header("Clustering")
        n_clusters = st.slider("Number of clusters", 2, 10, 4)
        sample_size = st.number_input("Max rows to use for plots", min_value=200, max_value=50000, value=5000, step=100)
        do_scale = st.checkbox("Scale features (recommended)", value=True)
        st.markdown("---")
        st.header("Export")
        download_name = st.text_input("Output CSV filename", value="uber_labeled.csv")

    # Load data
    df = None
    if upload is not None:
        try:
            df = pd.read_csv(upload, low_memory=False)
            st.success("Loaded uploaded CSV")
        except Exception as e:
            st.error(f"Failed to read uploaded CSV: {e}")
    else:
        try:
            df = load_data_from_path(csv_path)
            st.info(f"Loaded CSV from: {csv_path}")
        except FileNotFoundError:
            st.warning(f"CSV not found at {csv_path}. Upload a file or provide a valid path.")
        except Exception as e:
            st.error(f"Error loading CSV: {e}")

    if df is None or df.empty:
        st.stop()

    # Summary
    st.subheader("Data summary")
    c1, c2, c3 = st.columns([1, 2, 2])
    with c1:
        st.metric("Rows", int(len(df)))
        st.metric("Columns", int(len(df.columns)))
    with c2:
        st.write(df.head(5))
    with c3:
        missing = df.isna().sum()
        st.write(missing[missing > 0])

    # Ensure fare & distance
    if not {"fare", "distance_km"}.issubset(df.columns):
        st.error("Dataset must contain numeric fare and distance_km (or travel coords). See loader expectations.")
        st.stop()

    # Run clustering
    labels, kmeans, scaler = run_clustering(df, int(n_clusters), scale=do_scale)
    df["cluster"] = labels.astype(int)

    st.subheader("Clustering quality")
    if len(df) >= 2 and len(set(labels)) > 1:
        try:
            s_score = silhouette_score(df[["fare", "distance_km"]].to_numpy(), labels)
            st.write(f"Silhouette score (unscaled): {s_score:.3f}")
        except Exception:
            st.write("Silhouette score could not be computed on the raw features.")
    else:
        st.write("Silhouette score requires at least 2 clusters and >1 sample.")

    # Scatter
    st.subheader("Fare vs Distance")
    plot_df = df.sample(n=min(len(df), int(sample_size)), random_state=1)
    fig = px.scatter(
        plot_df,
        x="fare",
        y="distance_km",
        color=plot_df["cluster"].astype(str),
        labels={"fare": "Fare (USD)", "distance_km": "Distance (km)"},
        title=f"Fare vs Distance colored by {n_clusters} clusters",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Map (if coords available)
    if {"pickup_latitude", "pickup_longitude"}.issubset(df.columns):
        st.subheader("Pickup locations (sampled)")
        map_df = df.dropna(subset=["pickup_latitude", "pickup_longitude"]).sample(n=min(len(df), 2000), random_state=1)
        try:
            map_df = map_df.rename(columns={"pickup_latitude": "lat", "pickup_longitude": "lon"})
            st.map(map_df[["lat", "lon"]])
        except Exception:
            st.write("Map failed to render.")

    # Cluster centers table
    if st.checkbox("Show cluster centers (approx.)"):
        centers_scaled = kmeans.cluster_centers_
        if scaler is not None:
            centers = scaler.inverse_transform(centers_scaled)
        else:
            centers = centers_scaled
        centers_df = pd.DataFrame(centers, columns=["fare", "distance_km"])
        centers_df["cluster"] = centers_df.index
        st.table(centers_df)

    # Download
    st.subheader("Export labeled data")
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV with cluster labels", data=csv_bytes, file_name=download_name, mime="text/csv")


if __name__ == "__main__":
    app()
