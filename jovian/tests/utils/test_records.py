from unittest import TestCase, mock
from jovian.utils.records import get_record_slugs, reset_records, log_hyperparams, log_metrics, log_dataset, log_git
import jovian.utils.records
_d = jovian.utils.records._data_blocks


class FakeRecords(TestCase):
    def setUp(self):
        jovian.utils.records._data_blocks = [('fake_slug_metrics_1', 'metrics'),
                                             ('fake_slug_metrics_2', 'metrics'),
                                             ('fake_slug_hyperparams_1', 'hyperparams'),
                                             ('fake_slug_hyperparams_2', 'hyperparams')]

    def tearDown(self):
        jovian.utils.records._data_blocks = _d


class TestGetRecordSlugs(FakeRecords):
    def test_get_record_slugs_without_type(self):
        expected_result = ['fake_slug_metrics_1',
                           'fake_slug_metrics_2',
                           'fake_slug_hyperparams_1',
                           'fake_slug_hyperparams_2']

        self.assertEqual(get_record_slugs(), expected_result)

    def test_get_record_slugs_with_type(self):
        expected_result = [('fake_slug_metrics_1', 'metrics'),
                           ('fake_slug_metrics_2', 'metrics'),
                           ('fake_slug_hyperparams_1', 'hyperparams'),
                           ('fake_slug_hyperparams_2', 'hyperparams')]
        self.assertEqual(get_record_slugs(with_type=True), expected_result)


class TestResetRecords(FakeRecords):
    def test_reset_records(self):
        reset_records()
        expected_result = []
        self.assertEqual(jovian.utils.records._data_blocks, expected_result)

    def test_reset_records_metrics(self):
        reset_records('metrics')
        expected_result = [('fake_slug_hyperparams_1', 'hyperparams'),
                           ('fake_slug_hyperparams_2', 'hyperparams')]
        self.assertEqual(jovian.utils.records._data_blocks, expected_result)

    def test_reset_records_hyperparams(self):
        reset_records('hyperparams')
        expected_result = [('fake_slug_metrics_1', 'metrics'),
                           ('fake_slug_metrics_2', 'metrics')]
        self.assertEqual(jovian.utils.records._data_blocks, expected_result)


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


class TestLogHyperparams(FakeRecords):

    @mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
    def test_log_hyperparams(self, mock_api_post_block):
        data = {
            'arch_name': 'cnn_1',
            'lr': .001
        }
        expected_result = [('fake_slug_metrics_1', 'metrics'),
                           ('fake_slug_metrics_2', 'metrics'),
                           ('fake_slug_hyperparams_1', 'hyperparams'),
                           ('fake_slug_hyperparams_2', 'hyperparams'),
                           ('fake_slug_3', 'hyperparams')]

        log_hyperparams(data)
        self.assertEqual(jovian.utils.records._data_blocks, expected_result)


class TestLogMetrics(FakeRecords):

    @mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
    def test_log_metrics(self, mock_api_post_block):
        data = {
            'acc': 0.89,
            'val_acc': 0.86
        }
        expected_result = [('fake_slug_metrics_1', 'metrics'),
                           ('fake_slug_metrics_2', 'metrics'),
                           ('fake_slug_hyperparams_1', 'hyperparams'),
                           ('fake_slug_hyperparams_2', 'hyperparams'),
                           ('fake_slug_3', 'metrics')]

        log_metrics(data)
        self.assertEqual(jovian.utils.records._data_blocks, expected_result)


class TestLogDataset(FakeRecords):

    @mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
    def test_log_metrics(self, mock_api_post_block):
        data = {
            'col1': [1, 2, 3],
            'col2': [4, 5, 6]
        }
        expected_result = [('fake_slug_metrics_1', 'metrics'),
                           ('fake_slug_metrics_2', 'metrics'),
                           ('fake_slug_hyperparams_1', 'hyperparams'),
                           ('fake_slug_hyperparams_2', 'hyperparams'),
                           ('fake_slug_3', 'dataset')]

        log_dataset(data)
        self.assertEqual(jovian.utils.records._data_blocks, expected_result)


class TestLogGit(FakeRecords):

    @mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
    def test_log_metrics(self, mock_api_post_block):
        data = {
            'branch': 'sample_branch',
            'commit': 'sample_commit_hash',
            'remote': 'https://github.com/rohitsanj/fakerepo'
        }

        expected_result = [('fake_slug_metrics_1', 'metrics'),
                           ('fake_slug_metrics_2', 'metrics'),
                           ('fake_slug_hyperparams_1', 'hyperparams'),
                           ('fake_slug_hyperparams_2', 'hyperparams'),
                           ('fake_slug_3', 'git')]

        log_git(data)
        self.assertEqual(jovian.utils.records._data_blocks, expected_result)


# Test verbose log of `log_hyperparams` and `log_metrics`

@mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
def test_log_hyperparams_verbose(mock_api_post_block, capsys):
    data = {
        'arch_name': 'cnn_1',
        'lr': .001
    }
    log_hyperparams(data)
    captured = capsys.readouterr()

    expected_result = '[jovian] Hyperparameters logged.'
    assert expected_result == captured.out.strip()


@mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
def test_log_metrics_verbose(mock_api_post_block, capsys):
    data = {
        'acc': 0.89,
        'val_acc': 0.86
    }
    log_metrics(data)
    captured = capsys.readouterr()

    expected_result = '[jovian] Metrics logged.'
    assert expected_result == captured.out.strip()


@mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
def test_log_dataset_verbose(mock_api_post_block, capsys):
    data = {
        'col1': [1, 2, 3],
        'col2': [4, 5, 6]
    }
    log_dataset(data)
    captured = capsys.readouterr()

    expected_result = '[jovian] Dataset logged.'
    assert expected_result == captured.out.strip()


@mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
def test_log_git_verbose(mock_api_post_block, capsys):
    data = {
        'branch': 'sample_branch',
        'commit': 'sample_commit_hash',
        'remote': 'https://github.com/rohitsanj/fakerepo'
    }
    log_git(data)
    captured = capsys.readouterr()

    expected_result = '[jovian] Git information logged.'
    assert expected_result == captured.out.strip()
