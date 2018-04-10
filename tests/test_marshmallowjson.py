"""Tests for `marshmallowjson` package."""

import os
import json
import pytest

from marshmallowjson import Definition


@pytest.fixture
def email():
    schema = {
        'Person': {
            'email': {
                'kind': 'email',
                'required': True,
            }
        }
    }
    return Definition(schema).top()


@pytest.fixture
def lom():
    root = os.path.dirname(__file__)
    lom_path = os.path.join(root, 'data/lom.json')
    lom_file = open(lom_path)
    return Definition().from_file(lom_file)


@pytest.fixture
def full_nested_lom():
    root = os.path.dirname(__file__)
    lom_path = os.path.join(root, 'data/full_nested_lom.json')
    return json.load(open(lom_path))


def test_no_nested_to_full_nested_schema(lom, full_nested_lom):
    assert lom.to_full_nested() == full_nested_lom


def test_email_field_is_required(email):
    data, err = email.load({
        'not-email': 'definitively not an email'
    })
    assert not data
    assert 'email' in err


@pytest.mark.parametrize('example', ['ab.com', 'a+bc.com'])
def test_email_fails_with_invalid_email(email, example):
    data, err = email.load({
        'email': example
    })
    assert not data
    assert 'email' in err


@pytest.mark.parametrize('example', ['a@b.com', 'a+b@c.com'])
def test_email_passes_with_valid_email(email, example):
    data, err = email.load({
        'email': example
    })
    assert not err
    assert 'email' in data
    assert data['email'] == example
