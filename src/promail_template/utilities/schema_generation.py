from genson import SchemaBuilder  # type: ignore


class SchemaGen(SchemaBuilder):
    def __init__(self):
        self.add_schemea({"type": "object", "properties": {}})


builder = SchemaGen()

builder.add_object({"name": "Antoine"})
