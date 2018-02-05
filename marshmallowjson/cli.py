"""Console script for marshmallowjson."""

import sys

import click

from marshmallowjson import Definition, ValidationError


def echo(s, color='green'):
    """Echo click."""
    click.echo(click.style(s, fg=color))


@click.command()
@click.argument('definition', type=click.File('r'))
def main(definition):
    """Call marshmallowjson validation."""
    try:
        Definition.from_file(definition)
        echo('All clear')
    except ValidationError as e:
        echo(str(e), color='red')
        sys.exit(1)


if __name__ == "__main__":
    main()
