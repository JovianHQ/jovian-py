import os
import json
from unittest import TestCase, mock
from jovian.utils.constants import RC_FILENAME
from jovian.utils.rcfile import (rcfile_exists, save_rcdata, get_rcdata,
                                 get_notebook_slug, set_notebook_slug, make_rcdata)

data = {
    "notebooks": {
        "Testing Jovian.ipynb": {
            "slug": "46bd9a3f87e74de0baf8a6f0b60a8df9"
        }
    }
}


class RCFile(TestCase):
    def setUp(self):
        os.chdir('jovian/tests/resources/rcfile')

    def tearDown(self):
        os.chdir('../' * 4)


class CreateNewRCFile(RCFile):
    def setUp(self):
        super().setUp()
        with open(RC_FILENAME, 'w') as f:
            json.dump(data, f, indent=2)

    def tearDown(self):
        os.system('rm .jovianrc')
        super().tearDown()


class TestRCFileDoesNotExist(RCFile):

    def test_rcfile_does_not_exist(self):
        self.assertFalse(rcfile_exists())


class TestSaveRCData(RCFile):

    def test_save_rcdata_data_none(self):
        save_rcdata(data=None)
        expected_result = {
            "notebooks": {}
        }
        with open(RC_FILENAME, 'r') as f:
            self.assertEqual(json.load(f), expected_result)

    def test_save_rcdata_data_exists(self):
        save_rcdata(data=data)
        expected_result = data

        with open(RC_FILENAME, 'r') as f:
            self.assertEqual(json.load(f), expected_result)


class TestGetRCDataRCFileNotExist(RCFile):

    @mock.patch('jovian.utils.rcfile.rcfile_exists', mock.Mock(return_value=False))
    def test_get_rcdata_rcfile_does_not_exist(self):
        expected_result = {
            "notebooks": {}
        }
        self.assertEqual(get_rcdata(), expected_result)


class TestGetRCData(RCFile):

    def test_get_rcdata_rcfile_exists(self):
        with open(RC_FILENAME, 'w') as f:
            json.dump(data, f, indent=2)

        expected_result = data

        self.assertEqual(get_rcdata(), expected_result)

    def tearDown(self):
        os.system('rm .jovianrc')
        super().tearDown()


class TestGetNotebookSlug(CreateNewRCFile):

    def test_get_notebook_slug_notebook_present(self):
        filename = "Testing Jovian.ipynb"
        expected_result = "46bd9a3f87e74de0baf8a6f0b60a8df9"

        self.assertEqual(get_notebook_slug(filename), expected_result)

    def test_get_notebook_slug_notebook_not_present(self):
        filename = "Testing Jovian123.ipynb"
        expected_result = None

        self.assertEqual(get_notebook_slug(filename), expected_result)


class TestSetNotebookSlug(CreateNewRCFile):

    def test_set_notebook_slug_new_entry(self):
        filename = "Testing Jovian 2.ipynb"
        slug = "46bd9a3f87e74de0baf8a6f0b60a8df9"

        expected_result = {
            "notebooks": {
                "Testing Jovian.ipynb": {
                    "slug": "46bd9a3f87e74de0baf8a6f0b60a8df9"
                },
                "Testing Jovian 2.ipynb": {
                    "slug": "46bd9a3f87e74de0baf8a6f0b60a8df9"
                }
            }
        }

        set_notebook_slug(filename, slug)
        self.assertEqual(get_rcdata(), expected_result)

    def test_set_notebook_slug_existing_entry(self):
        filename = "Testing Jovian.ipynb"
        slug = "46bd9a3f87e74de0baf8a6f0b60a8df9"

        expected_result = data

        set_notebook_slug(filename, slug)
        self.assertEqual(get_rcdata(), expected_result)


class TestMakeRCData(CreateNewRCFile):
    def test_make_rcdata(self):
        filename = "Testing Jovian.ipynb"
        slug = "46bd9a3f87e74de0baf8a6f0b60a8df9"
        expected_result = '{"notebooks": {"Testing Jovian.ipynb": {"slug": "46bd9a3f87e74de0baf8a6f0b60a8df9"}}}'

        self.assertEqual(make_rcdata(filename, slug), expected_result)
