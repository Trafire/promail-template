import json
import os

import jinja2
from jinja2 import Environment, select_autoescape, FileSystemLoader
from jinja2 import Template
from jsonschema import validate

from promail_template.template import PromailTemplate


class HelloWorld(PromailTemplate):
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
        },
    }
    env = Environment(loader=FileSystemLoader(
        searchpath=os.path.dirname(os.path.abspath(__file__))),
        autoescape=select_autoescape(['mjml'])) #todo: make this a PromailTemplate.method that always find the folder of the current file

    mjml = r"hello_world.mjml"

    def __init__(self, data: dict = None, json_filepath: str = None):
        if data is None:
            if json_filepath is None:
                Exception(
                    "Must provide either a data or a json_field attribute")
            else:
                with open(json_filepath, 'r') as jsonfile:
                    self.user_data = json.load(jsonfile)

        else:
            self.user_data = data
        print(HelloWorld.schema)
        print(validate(instance=self.user_data, schema=HelloWorld.schema))
        self._context = None

    @property
    def context(self) -> dict:
        """Processes user data and expands on referenced fields (such as csvs)

        :return:
        """
        if self._context is None:
            self._context = self.user_data # todo: Process CSVs
        return self._context

    def render(self):
        # with open(HelloWorld.mjml) as f:
        template = HelloWorld.env.get_template(HelloWorld.mjml)

        return template.render(**self.context)  # this is where to put args to the template renderer


h = HelloWorld(data={"name": "Antoine"})
print(h.render())