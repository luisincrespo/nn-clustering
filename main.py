import argparse

from distances import Distances
from nearest_neighbor import NearestNeighbor


def pretty_print_clusters(clusters):
    string_buffer = []
    for index, cluster in enumerate(clusters):
        string_buffer.append('Cluster {}\n'.format(index + 1))
        for elem in cluster:
            string_buffer.append('\t - {}\n'.format(elem[1]))
    return ''.join(string_buffer)


def prepare_data(data_file, data_info_file):
    # the data file is assumed to hold one
    # line per instance, with attribute values separated
    # by comma
    with open(data_file, 'r') as f:
        data = []
        data_lines = f.readlines()
        for line in data_lines:
            data.append(line.split(','))
        f.close()

    # a supplementary data info file is expected
    # to hold one line per attribute, with
    # comma-separated values in the form:
    # <attribute_name>,<attribute_type>,<possible_values>
    # where <attribute_type> is one of 'nominal', 'ordinal', 'numeric',
    # 'binary_symmetric', 'binary_asymmetric'
    # <possible_values> can be omitted
    with open(data_info_file, 'r') as f:
        data_info = [{
            'name': 'ID',
            'type': 'identifier'
        }]
        data_info_lines = f.readlines()
        for line in data_info_lines:
            info = {}
            line = line.split(',')
            info['name'] = line[0]
            info['type'] = line[1]
            if len(line) > 2:
                info['possible_values'] = line[2]
            data_info.append(info)
        f.close()

    # - convert 'numeric' values to float
    # - replace missing '?' values with None
    for row in data:
        for i in range(0, len(row)):
            if data_info[i]['type'] == 'numeric':
                row[i] = float(row[i])
            if row[i] == '?':
                row[i] = None

    return data, data_info


def main():
    parser = argparse.ArgumentParser(description='Cluster data using Nearest'
                                                 ' Neighbor algorithm.')
    parser.add_argument('--datafile', dest='data_file', type=str,
                        required=True,
                        help='absolute or relative path to data file')
    parser.add_argument('--datainfofile', dest='data_info_file', type=str,
                        required=True,
                        help='absolute or relative path to data info file')
    parser.add_argument('--threshold', dest='threshold', type=float,
                        required=True,
                        help='threshold to be used by the algorithm'
                        ' (should be value between 0..1)')
    parser.add_argument('--outputfile', dest='output_file', type=str,
                        help='absolute or relative path to file where'
                             ' results should be written (if not'
                             ' specified results are printed in stdout)')
    args = parser.parse_args()

    data, data_info = prepare_data(args.data_file, args.data_info_file)
    distances = Distances(data, data_info).get_distances()
    clusters = NearestNeighbor(data, distances, args.threshold).get_clusters()

    printed_clusters = pretty_print_clusters(clusters)
    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(printed_clusters)
            f.close()
    else:
        print printed_clusters


if __name__ == '__main__':
    main()
