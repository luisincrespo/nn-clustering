class NearestNeighbor(object):
    def __init__(self, data, distances, threshold):
        self._data = data
        self._distances = distances
        self._threshold = threshold

    def get_clusters(self):
        clusters = [
            [(0, self._data[0][0])]
        ]
        for i in range(1, len(self._data)):
            min_distance = None
            selected_cluster_index = None
            for cluster_index, cluster in enumerate(clusters):
                cluster_min_distance = None
                for elem in cluster:
                    distance = self._distances[elem[0]][i]
                    if (cluster_min_distance is None or
                            distance < cluster_min_distance):
                        cluster_min_distance = distance
                if (min_distance is None or
                        cluster_min_distance < min_distance):
                    min_distance = cluster_min_distance
                    selected_cluster_index = cluster_index
            element = (i, self._data[i][0])
            if min_distance <= self._threshold:
                clusters[selected_cluster_index].append(element)
            else:
                clusters.append([element])
        return clusters
