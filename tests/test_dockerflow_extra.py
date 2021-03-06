# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.

import json
import mock
import io

import pytest
from requests.exceptions import ConnectionError
from jsonschema import ValidationError
from django.core.management import call_command

from buildhub.main.models import Build
from buildhub.dockerflow_extra import check_elasticsearch


def test_check_elasticsearch(elasticsearch):
    """This is a fully functional test that requires a healthy Elasticsearch
    connection."""
    elasticsearch.flush()
    errors = check_elasticsearch(None)
    assert not errors


def test_check_elasticsearch_connection_error(mocker):
    mocked_fetch = mocker.patch("buildhub.dockerflow_extra.fetch")

    def mocked_side_effect(index):
        raise ConnectionError("Oh no!")

    mocked_fetch.side_effect = mocked_side_effect
    errors = check_elasticsearch(None)
    assert errors
    error, = errors
    assert 'Unable to connect to Elasticsearch' in error.msg


def test_check_elasticsearch_failed_health(mocker):
    mocked_fetch = mocker.patch("buildhub.dockerflow_extra.fetch")

    def mocked_side_effect(index):
        return "Not looking good"

    mocked_fetch.side_effect = mocked_side_effect
    errors = check_elasticsearch(None)
    assert errors
    error, = errors
    assert 'not healthy' in error.msg
    assert 'Not looking good' in error.msg


