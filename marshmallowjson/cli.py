"""Console script for marshmallowjson."""

import click
import json
import sys


@click.command()
@click.argument('definition', type=click.File('r'))
def main(definition):
    """Validate an schema for marshmallow json"""
    known = set('string boolean uuid number integer decimal'.split())
    definitions = json.load(definition)
    for type_, schema in definitions.items():
        for name, field in schema.items():
            kind = field['kind']
            if kind not in known:
                click.echo(click.style(
                    '{kind} is not a known type in {type_}.{name}'.format(
                        kind=kind,
                        type_=type_,
                        name=name,
                    ),
                    fg='red'
                ))
                sys.exit(1)
        known.add(type_)
    click.echo(click.style('All clear', fg='green'))


if __name__ == "__main__":
    main()
