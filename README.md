# Automatically detect aircraft go-arounds
This tool enables the automatic detection of go-around events in aircraft position data, and currently supports positions supplied from the `OpenSky network` interface. Multiprocessing is used to speed up the data throughput.

The tool will produce graphics showing the flight path and phase for every detected landing aircraft. Normal landings can be stored in one subdirectory, potential go-arounds in another.

Requires:

- Xavier Olive's `Traffic` library: https://github.com/xoolive/traffic
 
- Junzi Sun's `flight-data-processor` library: https://github.com/junzis/flight-data-processor

- The requests library: `pip install requests`

- The click library: `pip install click`

Usage:
First you must download aircraft data, which can be done using the `OpenSky_Get_Data` script. You can then point `GA_Detect` at the download location to scan for go-arounds.

### `Metars_Get_Data.py`

To download the METARS data for a given station and timespan, use the
`Metars_Get_Data.py` script.  This script uses defaults that
correspond to the ones used in the `OpenSky_Get_Data.py` script, thus
these two calls are equivalent:

```bash
python Metars_Get_Data.py
python Metars_Get_Data.py \
    --station=VABB --start-dt=2019-08-10 --end-dt=2019-08-21 \
    --outfile=VABB_METARS
```

### `OpenSky_Get_Data.py`:

Use the script's `--outdir` option so the the output directory. This defaults to `INDATA` in your current working directory.

Use `--n-jobs` to specify the number of concurrent retrievals from the OpenSky database. I have found that six works well, but this may be different for you.

The airport region to retrieve data for is specified with the `--airport` option.  The default is `VABB`, which will import Mumbai airport (VABB). You should create your own airport definition in the `./airports` directory.

The border region around the airport is manually specified (as `0.45 deg`) in `get_bounds()`. You may wish to change this.

Running the script without parameters defaults to downloading data for
the ``VABB`` airport between 2019-08-10 and 2019-08-21 and saving that
data into the `INDATA` directory in your working directory.  Thus,
these two calls are equivalent:

```bash
python OpenSky_Get_Data.py  # does the same thing as the next command:
python OpenSky_Get_Data.py \
    --airport=VABB --start-dt=2019-08-10 --end-dt=2019-08-21 \
    --outdir=INDATA --n-jobs=1
```

### `GA_Detect.py`

The script that runs the actual go-around events.

Data is read and written based on a top-level directory.  The default
is the current working directory, which can be overridden by passing
the `--top-dir` command-line option.

The file containing the appropriate METARS data can be passed using
the `--metars-file` option.

The airport can be specified using the `--airport` option.  See the
`OS_Airports` subpackage which contains the runway definitions for the
currently supported airports.

The `--n-files-proc` option specifies how many files to process
simultaneously. This should be changed to the optimal value for your
hardware.

The `--pool-proc` option specifies the number of multiprocessing
threads to use. I have found that this can be set slightly higher than
the number of cores available, as cores are not fully utilised anyway.

The `GA_Detect.py` command-line script uses a few defaults.  The
defaults are chosen to accommodate the defaults in the data fetching
scripts.  As such, these two calls are equivalent:

```bash
python GA_Detect.py  # does the same thing as the next command:
python GA_Detect.py \
    --top-dir=. --metars-file=VABB_METAR --airport=VABB
```

## Running tests

To run the included test suite, first install pytest via `pip install
pytest` and then run `pytest -s tests`.
