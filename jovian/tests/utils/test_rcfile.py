from unittest import TestCase, mock
from jovian.utils.constants import RC_FILENAME
from jovian.utils.rcfile import rcfile_exists, save_rcdata, get_rcdata, get_notebook_slug, set_notebook_slug

data = {
    "notebooks": {
        "Testing Jovian.ipynb": {
            "slug": "46bd9a3f87e74de0baf8a6f0b60a8df9"
        }
    }
}
json_data = """{
    "notebooks": {
        "Testing Jovian.ipynb": {
            "slug": "46bd9a3f87e74de0baf8a6f0b60a8df9"
        }
    }
}"""


class TestRCFileExists(TestCase):

    @mock.patch("jovian.utils.rcfile.os")
    def test_rcfile_exists(self, mock_os):
        rcfile_exists()
        mock_os.path.exists.assert_called_with(RC_FILENAME)


class TestSaveRCData(TestCase):
    @mock.patch("jovian.utils.rcfile.open", new_callable=mock.mock_open)
    @mock.patch("jovian.utils.rcfile.json.dump")
    def test_save_rcdata_none(self, mock_json, mock_file):
        save_rcdata(data=None)
        mock_json.assert_called_with({'notebooks': {}}, mock_file.return_value, indent=2)

    @mock.patch("jovian.utils.rcfile.open", new_callable=mock.mock_open)
    @mock.patch("jovian.utils.rcfile.json.dump")
    def test_save_rcdata_normal(self, mock_json, mock_file):
        save_rcdata(data=data)
        mock_json.assert_called_with(data, mock_file.return_value, indent=2)


class TestGetRCData(TestCase):
    @mock.patch("jovian.utils.rcfile.rcfile_exists", mock.Mock(return_value=True))
    @mock.patch("jovian.utils.rcfile.json.loads")
    @mock.patch("jovian.utils.rcfile.open", new_callable=mock.mock_open, read_data=json_data)
    def test_save_get_rcdata_normal(self, mock_open, mock_loads):
        self.assertEqual(get_rcdata(), mock_loads.return_value)


class TestGetNotebookSlug(TestCase):

    @mock.patch("jovian.utils.rcfile.get_rcdata", mock.Mock(return_value=data))
    def test_get_notebook_slug(self):
        filename = "Testing Jovian.ipynb"
        expected_result = "46bd9a3f87e74de0baf8a6f0b60a8df9"

        self.assertEqual(get_notebook_slug(filename), expected_result)


class TestSetNotebookSlub(TestCase):

    @mock.patch("jovian.utils.rcfile.get_rcdata", mock.Mock(return_value=data))
    @mock.patch("jovian.utils.rcfile.save_rcdata")
    def test_set_notebook_slug(self, mock_save_rcdata):
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
        mock_save_rcdata.assert_called_with(expected_result)
