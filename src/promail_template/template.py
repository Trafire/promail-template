import abc

import sys

import json
import os
from typing import Optional, AnyStr

from jinja2 import Environment, select_autoescape, FileSystemLoader
from mjml import mjml_to_html
from io import StringIO
import webbrowser


class PromailTemplate(abc.ABC):
    """Object for creating Email templates"""

    sample_filename = "sample.json"
    schema_filename = "schema.json"
    mjml_filename = "template.mjml"

    # class Methods

    @classmethod
    def path(cls) -> str:
        """Gets absolute path of the directory class's directory"""
        mypath = os.path.dirname(str(sys.modules[cls.__module__].__file__))
        return mypath

    @classmethod
    def mjml_path(cls) -> AnyStr:
        """Get Absolute path to template.mjml file"""
        return cls.absolute_path(cls.mjml_filename)

    @classmethod
    def sample_path(cls) -> AnyStr:
        """Get Absolute path to sample.json file"""
        return cls.absolute_path(cls.sample_filename)

    @classmethod
    def schema_path(cls) -> AnyStr:
        """Get Absolute path to schema.json file"""
        return cls.absolute_path(cls.schema_filename)

    @classmethod
    def absolute_path(cls, relative_path):
        """Get absolute path to specified file within template directory"""
        return os.path.join(cls.path(), relative_path)

    # instance methods

    def __init__(self, data: dict = None, json_filepath: str = None):

        if data is None:
            if json_filepath is None:
                # if no data or json_filepath is provided we use the sample data
                json_filepath = self.sample_filename

            with open(json_filepath, "r") as jsonfile:
                self.user_data = json.load(jsonfile)

        else:
            self.user_data = data

        self._context = None
        self._mjml = None
        self._errors = None
        self._html = None

    @property
    def schema(self) -> dict:
        schema_filename = os.path.join(self.path(), "schema.json")
        with open(schema_filename, "r") as file:
            return json.load(file)

    @property
    def env(self):
        return Environment(
            loader=FileSystemLoader(searchpath=self.path()),
            autoescape=select_autoescape(["mjml"]),
        )

    @property
    def context(self) -> Optional[dict]:
        """Processes user data and expands on referenced fields (such as csv)

        :return:
        """
        if self._context is None:
            self._context = self.user_data  # todo: Process CSVs
        return self._context

    @property
    def mjml(self):
        if self._mjml is None:
            template = self.env.get_template(self.mjml_filename)
            self._mjml = template.render(
                **self.context
            )  # this is where to put args to the template renderer
        return self._mjml

    @property
    def html(self):
        if self._html is None:
            render_html = mjml_to_html(StringIO(self.mjml))
            self._html = render_html["html"]
            self._errors = render_html["errors"]
        return self._html

    def save_preview_html(self, path: str):
        """Saves a copy of html code at specified path
        Args:
            path:

        Returns:
        """
        with open(path, "w") as file:
            file.write(self.html)

    def preview_html(self, filename: str = "preview.html"):
        path = os.path.join(os.getcwd(), filename)
        self.save_preview_html(path)
        url = "file://" + path
        webbrowser.open(url)
