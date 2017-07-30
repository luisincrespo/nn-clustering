def get_clusters(data, distances, threshold):
    clusters = [
        [(0, data[0][0])]
    ]
    for i in range(1, len(data)):
        min_distance = None
        selected_cluster = None
        for cluster_index, cluster in enumerate(clusters):
            cluster_min_distance = None
            for elem in cluster:
                distance = distances[elem[0]][i]
                if (cluster_min_distance is None or
                        distance < cluster_min_distance):
                    cluster_min_distance = distance
            if (min_distance is None or
                    cluster_min_distance < min_distance):
                min_distance = cluster_min_distance
                selected_cluster = cluster_index
        if min_distance <= threshold:
            clusters[selected_cluster].append((i, data[i][0]))
        else:
            clusters.append([(i, data[i][0])])
    return clusters
