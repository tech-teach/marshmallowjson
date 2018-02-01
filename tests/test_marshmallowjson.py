"""Tests for `marshmallowjson` package."""

import os
import pytest

from click.testing import CliRunner

from marshmallowjson import marshmallowjson
from marshmallowjson import cli


@pytest.fixture
def unknown():
    root = os.path.dirname(__file__)
    return os.path.join(root, 'data/unknown.json')


@pytest.fixture
def basic():
    root = os.path.dirname(__file__)
    return os.path.join(root, 'data/basic.json')


@pytest.fixture
def list_schema():
    root = os.path.dirname(__file__)
    return os.path.join(root, 'data/list.json')


def test_error_when_using_unknown_type(unknown):
    runner = CliRunner()
    result = runner.invoke(cli.main, [unknown])
    assert result.exit_code == 1, result.output
    assert 'Unknown is not a known kind in Type.field' in result.output


def test_all_basic_types_are_allowed(basic):
    runner = CliRunner()
    result = runner.invoke(cli.main, [basic])
    assert result.exit_code == 0, result.output


def test_lists_are_allowed(list_schema):
    runner = CliRunner()
    result = runner.invoke(cli.main, [list_schema])
    assert result.exit_code == 0, result.output


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_avoid_warning():
    assert marshmallowjson is not None
