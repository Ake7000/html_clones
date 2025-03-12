import numpy as np
from sklearn.cluster import DBSCAN

def grupare(asemanari_combinate, eps, min_samples):
    asemanari_combinate = np.clip(asemanari_combinate, 0, 1)
    distance_matrix = 1 - asemanari_combinate
    clustering = DBSCAN(eps = eps, min_samples = min_samples, metric = 'precomputed')

    #creating labels for clustering
    labels = clustering.fit_predict(distance_matrix)
    return labels