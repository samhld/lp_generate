# lp_generate

##  Generates metrics in a format and method determined by the user.
InfluxCloud 2.0 has 2 cost vectors related to write volume: "Data In" and "Storage".  Predicting and/or generating the cost of payloads from the "Data In" perspective is trivial arithmetic.  However, storage is drastically affected by the "shape" of the data, itself.

InfluxDB deals with Tags and Fields differently.  It also deals with different Field types differently.  The compression alogrithms and, therefore, efficacy is different whether you write integers, floats, strings, booleans, etc.  Time stamp regularity and precision also affects compression.  

This command line application is designed to help generate a use case specific write workload that results in empirical evidence for what the write and storage costs will be to a user.

### Requires:
* Python 3.6+

### Usage:
(Currently this only prints to `stdout`.  I will be adding the ability to write to an InfluxDB endpoint shortly)
- **Command line**
  - `cd` into the `lp_generate` directory.
  - Run `<your Python 3.6+ interpreter> main.py <args>`
  - Arguments are optional as they have defaults.
  - Arguments are as follows:
    - `measurement`:        InfluxDB Measurement name to use for all Lines in a batch.
    - `--batch_size`:       Number of Lines to write in a single batch
    - `--num_tags`:         Number of InfluxDB Tags on each Line
    - `--int_fields`:       Number of Fields of type `int` on each Line
    - `--float_fields`:     Number of Fields of type `float` on each Line
    - `--str_fields`:       Number of Fields of type `string` on each Line
    - `--tag_key_size`:     Length of Tag keys on each Line
    - `--tag_value_size`:   Length of Tag values on each Line
    - `--field_key_size`:   Length of Field keys on each line
    - `--int_value_size`:   Length of `int` Field values on each Line
    - `--float_value_size`: Length of `float` Field values on each Line
    - `--str_value_size`:   Length of `string` Field values on each Line
    - `--precision`:        Timestamp precision: can be in `seconds`, `milliseconds`, `microseconds`, or `nanoseconds`
- **To do**
  - Configure for writing to InfluxDB