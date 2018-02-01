"""Console script for marshmallowjson."""

import sys

import click

from marshmallowjson.marshmallowjson import validate


def fail(kind, type_, name):
    """Fail error."""
    echo_error(
        '{kind} is not a known type in {type_}.{name}'.format(
            kind=kind,
            type_=type_,
            name=name,
        )
    )
    sys.exit(1)


def echo_error(s):
    """Echo click error."""
    click.echo(click.style(s, fg='red'))


def echo(s):
    """Echo click."""
    click.echo(click.style(s, fg='green'))


@click.command()
@click.argument('definition', type=click.File('r'))
def main(definition):
    """Call marshmallowjson validation."""
    try:
        validate(definition)
        echo('All clear')
    except Exception as e:
        echo_error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
