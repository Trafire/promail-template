import click

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main():
    """Promail Template"""
    click.echo("Hello, world!")
