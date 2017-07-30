import argparse
import pprint

from distances import get_distances
from cluster import get_clusters


def prepare_data(data_file, data_info_file):
    with open(data_file, 'r') as f:
        data = []
        data_lines = f.readlines()
        for line in data_lines:
            data.append(line.split(','))
        f.close()

    with open(data_info_file, 'r') as f:
        data_info = [{
            'name': 'ID',
            'type': 'identifier'
        }]
        data_info_lines = f.readlines()
        for line in data_info_lines[1:]:
            info = {}
            line = line.split(',')
            info['name'] = line[0]
            info['type'] = line[1]
            info['possible_values'] = line[2]
            data_info.append(info)
        f.close()

    for row in data:
        for i in range(0, len(row)):
            if data_info[i]['type'] == 'numeric':
                row[i] = float(row[i])

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
                        help='threshold to be used by the algorithm')
    parser.add_argument('--outputfile', dest='output_file', type=str,
                        help='absolute or relative path to file where'
                             ' results should be written (if not'
                             ' specified results are printed in stdout)')
    args = parser.parse_args()

    data, data_info = prepare_data(args.data_file, args.data_info_file)
    distances = get_distances(data, data_info)
    clusters = get_clusters(data, distances, args.threshold)
    if args.output_file:
        with open(args.output_file, 'w') as f:
            pprint.pprint(clusters, f)
            f.close()
    else:
        pprint.pprint(clusters)


if __name__ == '__main__':
    main()
