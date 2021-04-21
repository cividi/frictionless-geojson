import json
import tempfile
from decimal import Decimal
from frictionless import (
    Plugin,
    Parser,
    Dialect,
    Resource,
    Metadata,
    system,
    helpers,
    errors,
)
from frictionless.plugins.inline import InlineDialect
from frictionless.exception import FrictionlessException
from shapely.geometry import shape
import shapely.wkt
import shapely.wkb
import shapely.geometry


class GeoJsonPlugin(Plugin):

    code = "geojson"

    def create_dialect(self, resource, *, descriptor):
        if resource.format == "geojson":
            return GeoJsonDialect(descriptor)

    def create_parser(self, file):
        if file.format == "geojson":
            return GeoJsonParser(file)


# Dialect


class GeoJsonDialect(Dialect):
    """GeoJson dialect representation
    Parameters:
        descriptor? (str|dict): descriptor
        keys? (str[]): a list of strings to use as data keys
        geomRepresentation (str): geometry conversion: WKT
    Raises:
        FrictionlessException: raise any error that occurs during the process
    """

    def __init__(
        self,
        descriptor=None,
        *,
        keys=None,
        geomRepresentation="WKT",
    ):
        self.setinitial("keys", keys)
        self.setinitial("geomRepresentation", geomRepresentation)
        super().__init__(descriptor)

    @Metadata.property
    def keys(self):
        """
        Returns:
            str[]?: keys
        """
        return self.get("keys")

    @Metadata.property
    def geomRepresentation(self):
        """
        Returns:
            str?: geomRepresentation
        """
        # TODO: not yet settable by using a dialect
        return self.get("geomRepresentation")

    # Expand

    # def expand(self):
    #     """Expand metadata"""
    # self.setdefault("keyed", self.keyed)

    # Metadata

    metadata_profile = {  # type: ignore
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "keys": {"type": "array"},
            "geomRepresentation": {"type": "string"},
        },
    }


class GeoJsonParser(Parser):
    """GeoJson parser implementation."""

    requires_loader = True

    # Read

    def read_geojson(self, source_generator):
        for row in source_generator:
            # if self.resource.dialect.geomRepresentation == "GeoJson":
            #    geom = json.dumps(row["geometry"], cls=DecimalEncoder)
            if self.resource.dialect.geomRepresentation == "WKT":
                geom = shape(row["geometry"]).wkt
            # elif self.resource.dialect.geomRepresentation == "WKB":
            #    geom = shape(row["geometry"]).wkb
            yield {**row["properties"], "_geom": geom}

    def read_list_stream_create(self):
        ijson = helpers.import_from_plugin("ijson", plugin="json")
        dialect = self.resource.dialect
        try:
            source = ijson.items(self.loader.byte_stream, "features.item")
        except Exception:
            note = (
                f'''cannot extract GeoJSON tabular data
                from "{self.resource.fullpath}"'''
            )
            raise FrictionlessException(errors.SourceError(note=note))
        data = self.read_geojson(source)
        inline_dialect = InlineDialect(keys=dialect.keys)
        resource = Resource(data=data, dialect=inline_dialect)
        with system.create_parser(resource) as parser:
            try:
                yield next(parser.list_stream)
            except StopIteration:
                note = f'''cannot extract GeoJSON tabular data
                from "{self.resource.fullpath}"'''
                raise FrictionlessException(errors.SourceError(note=note))
            # if parser.resource.dialect.keyed:
            #     dialect["keyed"] = True
            yield from parser.list_stream

    # Write

    def write_row_stream(self, resource):
        data = {
            "type": "FeatureCollection",
            "features": [],
        }
        source = resource
        target = self.resource
        with source:
            for row in source.row_stream:
                item = {"type": "Feature", "properties": {}, "geometry": {}}
                cells = row.to_list(json=True)
                cell_items = dict(zip(row.field_names, cells))
                if self.resource.dialect.geomRepresentation == "WKT":
                    item["geometry"] = shapely.geometry.mapping(
                        shapely.wkt.loads(cell_items["_geom"])
                    )
                # elif self.resource.dialect.geomRepresentation == "WKB":
                #     item["geometry"] = shapely.geometry.mapping(
                #         shapely.wkb.loads(cell_items["_geom"]))
                # else:
                #     item["geometry"] = cell_items["_geom"]
                item["properties"] = {
                    k: v for k, v in cell_items.items() if k != "_geom"
                }
                data["features"].append(item)
        with tempfile.NamedTemporaryFile("wt", delete=False) as file:
            json.dump(data, file, indent=2)
        loader = system.create_loader(target)
        loader.write_byte_stream(file.name)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


system.register("geojson", GeoJsonPlugin())
