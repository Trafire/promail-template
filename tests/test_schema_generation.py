"""Test Schema Generator."""
from promail_template.utilities.schema_generation import SchemaGen


def test_schema_gen():
    """Test Schema Generator."""
    builder = SchemaGen()
    builder.add_object({"name": "Antoine"})
