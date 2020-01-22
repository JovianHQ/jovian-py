from unittest import TestCase, mock
from jovian.utils.records import get_records, reset, log_hyperparams, log_metrics, log_dataset, log_git, log_record
import jovian.utils.records


class FakeRecords(TestCase):
    def setUp(self):
        self._d = jovian.utils.records._data_blocks
        jovian.utils.records._data_blocks = [('fake_slug_metrics_1', 'metrics', {}),
                                             ('fake_slug_metrics_2', 'metrics', {}),
                                             ('fake_slug_hyperparams_1', 'hyperparams', {}),
                                             ('fake_slug_hyperparams_2', 'hyperparams', {})]

    def tearDown(self):
        jovian.utils.records._data_blocks = self._d


class TestGetRecords(FakeRecords):
    def test_get_records_without_type(self):
        expected_result = ['fake_slug_metrics_1',
                           'fake_slug_metrics_2',
                           'fake_slug_hyperparams_1',
                           'fake_slug_hyperparams_2']

        self.assertEqual(get_records(slug_only=True), expected_result)

    def test_get_records_with_type(self):
        expected_result = [('fake_slug_metrics_1', 'metrics', {}),
                           ('fake_slug_metrics_2', 'metrics', {}),
                           ('fake_slug_hyperparams_1', 'hyperparams', {}),
                           ('fake_slug_hyperparams_2', 'hyperparams', {})]
        self.assertEqual(get_records(), expected_result)


class TestReset(FakeRecords):
    def test_reset(self):
        reset()
        expected_result = []
        self.assertEqual(jovian.utils.records._data_blocks, expected_result)

    def test_reset_metrics(self):
        reset('metrics')
        expected_result = [('fake_slug_hyperparams_1', 'hyperparams', {}),
                           ('fake_slug_hyperparams_2', 'hyperparams', {})]
        self.assertEqual(jovian.utils.records._data_blocks, expected_result)

    def test_reset_hyperparams(self):
        reset('hyperparams')
        expected_result = [('fake_slug_metrics_1', 'metrics', {}),
                           ('fake_slug_metrics_2', 'metrics', {})]
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


class TestLogRecord(FakeRecords):
    @mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
    def test_log_record_no_data(self, mock_api_post_block):
        data = {}
        expected_result = [('fake_slug_metrics_1', 'metrics', {}),
                           ('fake_slug_metrics_2', 'metrics', {}),
                           ('fake_slug_hyperparams_1', 'hyperparams', {}),
                           ('fake_slug_hyperparams_2', 'hyperparams', {})]

        log_record('fake_record_type', data)
        self.assertEqual(jovian.utils.records._data_blocks, expected_result)


class TestLogHyperparams(FakeRecords):

    @mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
    def test_log_hyperparams(self, mock_api_post_block):
        data = {
            'arch_name': 'cnn_1',
            'lr': .001
        }
        expected_result = [('fake_slug_metrics_1', 'metrics', {}),
                           ('fake_slug_metrics_2', 'metrics', {}),
                           ('fake_slug_hyperparams_1', 'hyperparams', {}),
                           ('fake_slug_hyperparams_2', 'hyperparams', {}),
                           ('fake_slug_3', 'hyperparams', data)]

        log_hyperparams(data)
        self.assertEqual(jovian.utils.records._data_blocks, expected_result)


class TestLogMetrics(FakeRecords):

    @mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
    def test_log_metrics(self, mock_api_post_block):
        data = {'acc': 0.89, 'val_acc': 0.86}
        expected_result = [('fake_slug_metrics_1', 'metrics', {}),
                           ('fake_slug_metrics_2', 'metrics', {}),
                           ('fake_slug_hyperparams_1', 'hyperparams', {}),
                           ('fake_slug_hyperparams_2', 'hyperparams', {}),
                           ('fake_slug_3', 'metrics', data)]

        log_metrics(acc=0.89, val_acc=0.86)
        self.assertEqual(jovian.utils.records._data_blocks, expected_result)


class TestLogDataset(FakeRecords):

    @mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
    def test_log_dataset(self, mock_api_post_block):
        data = {
            'col1': [1, 2, 3],
            'col2': [4, 5, 6]
        }
        expected_result = [('fake_slug_metrics_1', 'metrics', {}),
                           ('fake_slug_metrics_2', 'metrics', {}),
                           ('fake_slug_hyperparams_1', 'hyperparams', {}),
                           ('fake_slug_hyperparams_2', 'hyperparams', {}),
                           ('fake_slug_3', 'dataset', data)]

        log_dataset(data)
        self.assertEqual(jovian.utils.records._data_blocks, expected_result)


class TestLogGit(FakeRecords):

    @mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
    def test_log_git(self, mock_api_post_block):
        data = {
            'branch': 'sample_branch',
            'commit': 'sample_commit_hash',
            'remote': 'https://github.com/rohitsanj/fakerepo'
        }

        expected_result = [('fake_slug_metrics_1', 'metrics', {}),
                           ('fake_slug_metrics_2', 'metrics', {}),
                           ('fake_slug_hyperparams_1', 'hyperparams', {}),
                           ('fake_slug_hyperparams_2', 'hyperparams', {}),
                           ('fake_slug_3', 'git', data)]

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

    expected_result = '[jovian] Hyperparams logged.'
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

    expected_result = '[jovian] Git logged.'
    assert expected_result == captured.out.strip()
