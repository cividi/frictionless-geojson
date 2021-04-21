[![Build](https://img.shields.io/github/workflow/status/cividi/frictionless-geojson/main/main)](https://github.com/cividi/frictionless-geojson/actions)
[![Coverage](https://img.shields.io/codecov/c/github/cividi/frictionless-geojson/main)](https://codecov.io/gh/cividi/frictionless-geojson)
[![Registry](https://img.shields.io/pypi/v/frictionless_geojson.svg)](https://pypi.python.org/pypi/frictionless_geojson)
[![Codebase](https://img.shields.io/badge/github-main-brightgreen)](https://github.com/cividi/frictionless-geojson)

# Frictionless GeoJSON

An extension to add [GeoJSON](https://geojson.org/geojson-spec.html) read and write support in [frictionless-py](https://framework.frictionlessdata.io).

## Guide

### Load the package

#### Release version

```sh
pip install frictionless_geojson
```

#### Dev version

```sh
python3 -V # should be > 3.6

# download project
git clone git@github.com:cividi/frictionless-geojson.git
cd frictionless-geojson

# Load dynamic dev version
make dev # or python3 -m pip install -e .
```

### Load GeoJSON and convert to CSV

```python
from frictionless import Resource
from pprint import pprint

# Load GeoJSON
data = Resource('<PATH-TO-GEOJSON>.geojson')

# Print out data
pprint(data.read_rows())

# Write CSV to disk - generates _geom column with WKT geometry
data.write('<PATH-TO-CSV>.csv')
```

### Load CSV with WKT `_geom` column and convert to GeoJSON

```python
from frictionless import Resource
from pprint import pprint

# Load CSV
data = Resource('<PATH-TO-CSV>.csv')

# Print out data
pprint(data.read_rows())

# Write GeoJSON to disk - requires _geom column with WKT geometry
data.write('<PATH-TO-GEOJSON>.geojson')
```
