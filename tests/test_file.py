from frictionless import system


def test_file_type_table():
    path = "data/geo.geojson"
    file = system.create_file(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "geo"
    assert file.type == "table"
    assert file.scheme == "file"
    assert file.format == "geojson"
    assert file.innerpath == ""
    assert file.compression == ""
    assert file.memory is False
    assert file.remote is False
    assert file.multipart is False
    assert file.basepath == ""
    assert file.fullpath == "data/geo.geojson"
