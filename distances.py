def get_attribute_min_max(index, data):
    # TODO: cache the return value of this function
    # because it'll be executed multiple times for
    # the same index and data
    minimum = maximum = data[0][index]
    for row in data:
        if row[index] < minimum:
            minimum = row[index]
        if row[index] > maximum:
            maximum = row[index]
    return minimum, maximum


def numeric_distance(i, j, index, data):
    value_1 = data[i][index]
    value_2 = data[j][index]
    minimum, maximum = get_attribute_min_max(index, data)
    return abs(value_1 - value_2) / float(maximum - minimum)


def nominal_distance(v1, v2):
    return 0 if v1 == v2 else 1


def get_distance(i, j, data, data_info):
    row_i = data[i]
    row_j = data[j]
    numerator = []
    denominator = []
    for x in range(0, len(row_i)):
        data_type = data_info[x]['type']
        v1 = row_i[x]
        v2 = row_j[x]

        if data_type == 'identifier':
            continue
        if v1 is None or v2 is None:
            continue
        if data_type == 'binary_asymmetric' and v1 == v2 == 0:
            continue

        if data_type == 'numeric':
            numerator.append(1 * numeric_distance(i, j, x, data))
        elif data_type in ['nominal', 'binary_symmetric', 'binary_asymmetric']:
            numerator.append(1 * nominal_distance(v1, v2))
        elif data_type == 'ordinal':
            # TODO: implement distance calc for ordinal attributes,
            # the complex thing here is related to the normalization
            # of rank values
            pass

        denominator.append(1)
    return sum(numerator) / float(sum(denominator))


def get_distances(data, data_info):
    distances = [[0 for _ in range(0, len(data))] for _ in range(0, len(data))]
    for i in range(0, len(data)):
        for j in range(i + 1, len(data)):
            distances[i][j] = distances[j][i] = \
                get_distance(i, j, data, data_info)
    return distances
