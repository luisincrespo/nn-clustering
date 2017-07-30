# Nearest Neighbor Clustering

## Requirements
- Python `2.7.x`

## Usage
```
$ python main.py --datafile <path_to_data> --datainfofile <path_to_data_info> --threshold <threshold>
```

- The values given to `--datafile` and `--datainfofile` can be either absolute or relative paths.
- The value of `--threshold` should be between 0..1.

The resulting clusters will be printed to `stdout` by default, but you can specify a path to a file to write results with the `--outputfile` option:
```
$ python main.py --datafile <path_to_data> --datainfofile <path_to_data_info> --threshold <threshold> --outputfile <path_to_outputfile>
```

## Expected data format
As stated above, the script expects two files:
- `--datafile` - the data set, which must be a `CSV` with each line of the form:
    > &lt;row_identifier&gt;,&lt;attr1_value&gt;,&lt;attr2_value&gt;,...

    Missing attribute values must be represented with the value `?`.

- `--datainfofile` - metadata that describes the data set, which must be a `CSV` with one line describing each attribute available in the data set:
    > &lt;attr_name&gt;,&lt;attr_type&gt;,&lt;attr_possible_values&gt;,...

    The supported values for `<attr_type>` are `nominal`, `ordinal`, `binary_symmetric`, `binary_asymmetric`, and `numeric`. The value for `<attr_possible_values>` may be omitted.

Example data can be found in the `example_data` folder, retrieved from http://archive.ics.uci.edu/ml/datasets/Sponge.
