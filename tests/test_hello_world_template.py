from promail_template.templates.full import HelloWorld
import os


def test_hello_world_template_path_exists() -> None:
    """Test that template folder has required files"""
    # data = {"name": "Antoine"}

    # folder exists
    assert os.path.exists(HelloWorld.path())
    # sample.json exists
    assert os.path.exists(HelloWorld.sample_path())
    # schema.json exists
    assert os.path.exists(HelloWorld.schema_path())
    # template.mjml exists
    assert os.path.exists(HelloWorld.mjml_path())


def test_valid_initialization():
    data = {"name": "Antoine"}
    HelloWorld(data)
