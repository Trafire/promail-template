"""Test Hello world example."""
import os

from promail_template.templates.full import HelloWorld

import pytest


def test_hello_world_template_path_exists() -> None:
    """Test that template folder has required files."""
    # data = {"name": "Antoine"}

    # folder exists
    assert os.path.exists(HelloWorld.path())
    # sample.json exists
    assert os.path.exists(HelloWorld.sample_path())
    # schema.json exists
    assert os.path.exists(HelloWorld.schema_path())
    # template.mjml exists
    assert os.path.exists(HelloWorld.mjml_path())


def test_valid_initialization_with_data():
    """Test Initialization."""
    data = {"name": "Antoine"}
    HelloWorld(data)


def test_initialization_no_data():
    """Test Initialization."""
    HelloWorld()


def test_initialization_with_path():
    """Test Initialization."""
    HelloWorld(json_filepath="tests/data/hello_world.json")


def test_path():
    """Test path."""
    data = {"name": "Antoine"}
    template = HelloWorld(data)
    assert template.path().endswith("hello_world")


def test_sample_path():
    """Test ""sample path."""
    assert HelloWorld.sample_path().endswith("sample.json")


def test_schema():
    """Test schema."""
    assert HelloWorld.schema_path().endswith("schema.json")
    assert HelloWorld.schema()["properties"]["name"]["type"] == "string"


def test_html():
    """Test html."""
    data = {"name": "Antoine"}
    template = HelloWorld(data)
    assert isinstance(template.html, str)

    template = HelloWorld()
    assert isinstance(template.html, str)


def test_context():
    """Test context."""
    data = {"name": "Antoine"}
    template = HelloWorld(data)
    assert isinstance(template.context, dict)


def test_mjml():
    """Test mjml."""
    template = HelloWorld()
    assert isinstance(template.mjml, str)


def test_sample_validation():
    """Test provided Sample data is valid."""
    data = HelloWorld.sample_data()
    HelloWorld.validate_data(data)


def test_schema_generation():
    """Test Schema Generation."""
    HelloWorld.generate_schema({"name": "World"})


def test_plaintext():
    """Test Plaintext."""
    HelloWorld().plaintext


@pytest.mark.e2e
def test_preview_html():
    """Test html preview."""
    template = HelloWorld()
    template.preview_html()
