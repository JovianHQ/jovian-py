from unittest import TestCase, mock
from jovian.utils.records import get_record_slugs, reset_records
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


# class TestLogHyperparams(FakeRecords):
