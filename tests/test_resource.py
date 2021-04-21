from frictionless import Resource, helpers

IS_UNIX = not helpers.is_platform("windows")


# General


def test_resource():
    resource = Resource("data/geo.geojson")
    assert resource.name == "geo"
    assert resource.fullpath == "data/geo.geojson" if IS_UNIX else "data\\geo.geojson"
    assert resource.profile == "tabular-data-resource"
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
