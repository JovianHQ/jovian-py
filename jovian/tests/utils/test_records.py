from unittest import TestCase, mock

import pytest

import jovian.utils.records
from jovian.tests.resources.shared import fake_records
from jovian.utils.records import get_records, log_dataset, log_git, log_hyperparams, log_metrics, log_record, reset

RECORDS = [('fake_slug_metrics_1', 'metrics', {}),
           ('fake_slug_metrics_2', 'metrics', {}),
           ('fake_slug_hyperparams_1', 'hyperparams', {}),
           ('fake_slug_hyperparams_2', 'hyperparams', {})]


def test_get_records_without_type():
    with fake_records():
        expected_result = ['fake_slug_metrics_1',
                           'fake_slug_metrics_2',
                           'fake_slug_hyperparams_1',
                           'fake_slug_hyperparams_2']

        assert get_records(slug_only=True) == expected_result


def test_get_records_with_type():
    with fake_records():
        expected_result = [('fake_slug_metrics_1', 'metrics', {}),
                           ('fake_slug_metrics_2', 'metrics', {}),
                           ('fake_slug_hyperparams_1', 'hyperparams', {}),
                           ('fake_slug_hyperparams_2', 'hyperparams', {})]
        assert get_records() == expected_result


@pytest.mark.parametrize(
    "metric_type, expected_result",
    [
        (
            ['metrics'],
            [('fake_slug_hyperparams_1', 'hyperparams', {}),
             ('fake_slug_hyperparams_2', 'hyperparams', {})]
        ),
        (
            ['hyperparams'],
            [('fake_slug_metrics_1', 'metrics', {}),
             ('fake_slug_metrics_2', 'metrics', {})]
        ),
        (
            ['metrics', 'hyperparams'],
            []
        ),
    ]
)
def test_reset(metric_type, expected_result):
    with fake_records():
        reset(*metric_type)
        assert jovian.utils.records._data_blocks == expected_result


def test_reset_all():
    with fake_records():
        reset()
        assert jovian.utils.records._data_blocks == []


def mock_api_post_block(*args, **kwargs):
    data = {
        'count': 1,
        'tracking': {
            'createdAt': 1577270059593,
            'updatedAt': None, 'gistSlug': None,
            'trackingSlug': 'fake_slug_3',
            'gistVersion': None
        }
    }

    return data


@mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
def test_log_record_no_data(mock_api_post_block):
    with fake_records():
        data = {}
        expected_result = RECORDS

        log_record('fake_record_type', data)
        assert jovian.utils.records._data_blocks == expected_result


@pytest.mark.parametrize(
    "data, func, metric_type",
    [
        (
            {'arch_name': 'cnn_1', 'lr': .001},
            log_hyperparams,
            'hyperparams',
        ),
        (
            {'acc': 0.89, 'val_acc': 0.86},
            log_metrics,
            'metrics',
        ),
        (
            {'col1': [1, 2, 3], 'col2': [4, 5, 6]},
            log_dataset,
            'dataset',
        ),
        (
            {
                'branch': 'sample_branch',
                'commit': 'sample_commit_hash',
                'remote': 'https://github.com/rohitsanj/fakerepo'
            },
            log_git,
            'git'
        ),
    ]
)
@mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
def test_log_records(mock_api_post_block, data, func, metric_type, capsys):
    with fake_records():
        func(data)
        assert jovian.utils.records._data_blocks == RECORDS + [('fake_slug_3', metric_type, data)]

        captured = capsys.readouterr()
        expected_result = '[jovian] {} logged.'.format(metric_type.capitalize())
        assert expected_result == captured.out.strip()


@pytest.mark.parametrize(
    "data, data_args, expected_result",
    [
        (
            {"key1": "value1"},
            {"key2": "value2"},
            {"key1": "value1", "key2": "value2"},
        ),
        (
            ["foo", "bar"],
            {"spam": "eggs"},
            ['foo', 'bar', {'spam': 'eggs'}],
        ),
    ]
)
@mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
def test_log_record_with_data_args(mock_api_post_block, data, data_args, expected_result):
    with fake_records():
        log_record('fake_record_type', data, **data_args)
        assert jovian.utils.records._data_blocks == RECORDS + [('fake_slug_3', 'fake_record_type', expected_result)]
