"""Tests for `marshmallowjson` package."""

import pytest
import json
import io

from marshmallowjson import marshmallowjson


@pytest.fixture
def email():
    file_ = io.StringIO()
    json.dump({
        'Person': {
            'email': {
                'kind': 'email',
                'required': True,
            }
        }
    }, file_)
    file_.seek(0)
    schema = marshmallowjson.from_file(file_)
    return schema


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
