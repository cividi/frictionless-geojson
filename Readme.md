# Frictionless GeoJSON

An extension to add [GeoJSON](https://geojson.org/geojson-spec.html) read and write support in [frictionless-py](https://framework.frictionlessdata.io).

## Guide

### Load the package

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
