class Distances(object):
    def __init__(self, data, data_info):
        self._data = data
        self._data_info = data_info
        self._memoized_atrributes_min_max = {}

    def _get_attribute_min_max(self, index):
        """
        Returns the minimum and maximum values at 'index' in the
        data.
        """
        if index in self._memoized_atrributes_min_max:
            return self._memoized_atrributes_min_max[index]

        minimum = maximum = self._data[0][index]
        for row in self._data:
            if row[index] < minimum:
                minimum = row[index]
            if row[index] > maximum:
                maximum = row[index]
        self._memoized_atrributes_min_max[index] = (minimum, maximum)
        return minimum, maximum

    def _numeric_distance(self, i, j, index):
        """
        Returns the normalized distance between the values at 'index' for rows
        'i','j' in the data.
        """
        value_1 = self._data[i][index]
        value_2 = self._data[j][index]
        minimum, maximum = self._get_attribute_min_max(index)
        return abs(value_1 - value_2) / float(maximum - minimum)

    def _nominal_distance(self, v1, v2):
        """
        Returns the distance between two nominal values.
        """
        return 0 if v1 == v2 else 1

    def _get_distance(self, i, j):
        """
        Returns the distance between rows 'i','j' in the data.
        Rows can be of mixed data types, supported data types
        are 'numeric', 'binary_asymmetric', 'binary_symmetric',
        'ordinal', 'nominal'.
        The special data type 'identifier' is simply ignored from
        the calculation.
        """
        row_i = self._data[i]
        row_j = self._data[j]
        numerator = []
        denominator = []
        for x in range(0, len(row_i)):
            data_type = self._data_info[x]['type']
            v1 = row_i[x]
            v2 = row_j[x]

            if data_type == 'identifier':
                continue
            if v1 is None or v2 is None:
                continue
            if data_type == 'binary_asymmetric' and v1 == v2 == 0:
                continue

            if data_type == 'numeric':
                numerator.append(1 * self._numeric_distance(i, j, x))
            elif (data_type in
                    ['nominal', 'binary_symmetric', 'binary_asymmetric']):
                numerator.append(1 * self._nominal_distance(v1, v2))
            elif data_type == 'ordinal':
                # TODO: implement distance calc for ordinal attributes,
                # the complex thing here is related to the normalization
                # of rank values
                pass

            denominator.append(1)
        return sum(numerator) / float(sum(denominator))

    def get_distances(self):
        """
        Returns a matrix of distances between each row in the data.
        The resultant matrix is symmetric, this is, a[i][j] == a[j][i].
        """
        distances = [
            [0 for _ in range(0, len(self._data))]
            for _ in range(0, len(self._data))
        ]
        for i in range(0, len(self._data)):
            for j in range(i + 1, len(self._data)):
                distances[i][j] = distances[j][i] = \
                    self._get_distance(i, j)
        return distances
