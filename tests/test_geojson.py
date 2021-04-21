from frictionless import Resource
from frictionless import describe_dialect

# Parser


def test_geojson_parser():
    with Resource("data/geo.geojson") as resource:
        assert resource.header == ["id", "name", "_geom"]
        assert resource.read_rows() == [
            {
                "id": 1,
                "name": "Polygon",
                "_geom": "POLYGON ((8.47771167755127 47.38199192001289, 8.495779037475586 47.38199192001289, 8.495779037475586 47.39091206104779, 8.47771167755127 47.39091206104779, 8.47771167755127 47.38199192001289))",
            },
            {
                "id": 2,
                "name": "LineString",
                "_geom": "LINESTRING (8.47771167755127 47.38199192001289, 8.495779037475586 47.38199192001289)",
            },
            {
                "id": 3,
                "name": "Point",
                "_geom": "POINT (8.47771167755127 47.38199192001289)",
            },
        ]


def test_geojson_parser_stream():
    source = open("data/geo.geojson", mode="rb")
    with Resource(source, format="geojson") as resource:
        assert resource.header == ["id", "name", "_geom"]
        assert resource.read_rows() == [
            {
                "id": 1,
                "name": "Polygon",
                "_geom": "POLYGON ((8.47771167755127 47.38199192001289, 8.495779037475586 47.38199192001289, 8.495779037475586 47.39091206104779, 8.47771167755127 47.39091206104779, 8.47771167755127 47.38199192001289))",
            },
            {
                "id": 2,
                "name": "LineString",
                "_geom": "LINESTRING (8.47771167755127 47.38199192001289, 8.495779037475586 47.38199192001289)",
            },
            {
                "id": 3,
                "name": "Point",
                "_geom": "POINT (8.47771167755127 47.38199192001289)",
            },
        ]


def test_geojson_parser_write_csv(tmpdir):
    source = Resource("data/geo.geojson")
    target = Resource(str(tmpdir.join("geo.csv")))
    source.write(target)
    with target:
        assert target.header == ["id", "name", "_geom"]
        assert target.read_rows() == [
            {
                "id": 1,
                "name": "Polygon",
                "_geom": "POLYGON ((8.47771167755127 47.38199192001289, 8.495779037475586 47.38199192001289, 8.495779037475586 47.39091206104779, 8.47771167755127 47.39091206104779, 8.47771167755127 47.38199192001289))",
            },
            {
                "id": 2,
                "name": "LineString",
                "_geom": "LINESTRING (8.47771167755127 47.38199192001289, 8.495779037475586 47.38199192001289)",
            },
            {
                "id": 3,
                "name": "Point",
                "_geom": "POINT (8.47771167755127 47.38199192001289)",
            },
        ]


def test_geojson_parser_write_geojson(tmpdir):
    source = Resource("data/geo_wkt.csv")
    target = Resource(str(tmpdir.join("geo.geojson")))
    source.write(target)
    with target:
        assert target.header == ["id", "name", "_geom"]
        assert target.read_rows() == [
            {
                "id": 1,
                "name": "Polygon",
                "_geom": "POLYGON ((8.47771167755127 47.38199192001289, 8.495779037475586 47.38199192001289, 8.495779037475586 47.39091206104779, 8.47771167755127 47.39091206104779, 8.47771167755127 47.38199192001289))",
            },
            {
                "id": 2,
                "name": "LineString",
                "_geom": "LINESTRING (8.47771167755127 47.38199192001289, 8.495779037475586 47.38199192001289)",
            },
            {
                "id": 3,
                "name": "Point",
                "_geom": "POINT (8.47771167755127 47.38199192001289)",
            },
        ]


def test_geojson_dialect():
    dialect = describe_dialect("data/geo.geojson")
    assert dialect == {"geomRepresentation": "WKT"}
