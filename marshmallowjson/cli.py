"""Console script for marshmallowjson."""

import click
import sys


@click.command()
@click.argument('schema', type=click.File('r'))
def main(schema):
    """Console script for marshmallowjson."""
    click.echo(click.style(
        'Unknown is not a known type in Type.field',
        fg='red'
    ))
    sys.exit(1)


if __name__ == "__main__":
    main()
