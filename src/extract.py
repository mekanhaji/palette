import numpy as np
from sklearn.cluster import KMeans


def cluster_pixels(pixels: np.ndarray, n_clusters: int = 6):
    print("Clustering pixels into {} clusters...".format(n_clusters))

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(pixels)

    print("Clustering completed.")
    return kmeans.labels_, kmeans.cluster_centers_
