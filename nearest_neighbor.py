class NearestNeighbor(object):
    def __init__(self, data, distances, threshold):
        self._data = data
        self._distances = distances
        self._threshold = threshold

    def get_clusters(self):
        # initialize single cluster with first row of data,
        # each element inside a cluster will be of the form
        # (<row_index>, <row_identifier>) where <row_identifier>
        # is assumed to be the first column of the row
        clusters = [
            [(0, self._data[0][0])]
        ]
        for i in range(1, len(self._data)):
            min_distance = None
            selected_cluster_index = None
            # we look for an element inside any cluster
            # which has the minimum distance to the current
            # element
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

            # once we have found the closest element (minimum distance)
            # to the current element, we decide:
            # - if minimum distance lower than or equal to threshold
            #   add current element to same cluster
            # - else create a new cluster with the current element
            element = (i, self._data[i][0])
            if min_distance <= self._threshold:
                clusters[selected_cluster_index].append(element)
            else:
                clusters.append([element])
        return clusters
