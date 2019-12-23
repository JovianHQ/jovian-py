from unittest import TestCase, mock

from jovian.utils.misc import (is_uuid, get_platform, get_file_extension, urljoin)
from jovian.utils.constants import LINUX, WINDOWS, MACOS


class TestIsUUID(TestCase):

    def test_is_uuid_without_hyphens(self):
        text = "374ab6086ca449769b3e44b6e35f9126"

        self.assertTrue(is_uuid(text))

    def test_is_uuid_with_hypens(self):
        text = "374ab608-6ca4-4976-9b3e-44b6e35f9126"

        self.assertTrue(is_uuid(text))

    def test_is_uuid_false(self):
        text = "this-is-not-a-uuid"

        self.assertFalse(is_uuid(text))


class TestGetFileExtension(TestCase):

    def test_get_file_extension_normal(self):
        file = "users/siddhant/file.ipynb"
        expected_result = "ipynb"

        self.assertEqual(get_file_extension(file), expected_result)

    def test_get_file_extension_malformed(self):
        file = 123
        expected_result = ''

        self.assertEqual(get_file_extension(file), expected_result)


class TestGetPlatform(TestCase):
    @mock.patch("platform.system", mock.Mock(return_value="Windows"))
    def test_get_platform_windows(self):
        self.assertEqual(get_platform(), WINDOWS)

    @mock.patch("platform.system", mock.Mock(return_value="Linux"))
    def test_get_platform_linux(self):
        self.assertEqual(get_platform(), LINUX)

    @mock.patch("platform.system", mock.Mock(return_value="Darwin"))
    def test_get_platform_macos(self):
        self.assertEqual(get_platform(), MACOS)


class UrlUtilsTest(TestCase):

    def test_urljoin_normal(self):
        base_url_1 = "https://jovian.ml"
        base_url_2 = "https://jovian.ml/"

        path_1 = "user/siddhant"
        path_2 = "/user/siddhant"

        expected_result = "https://jovian.ml/user/siddhant"

        self.assertEqual(urljoin(base_url_1, path_1), expected_result)
        self.assertEqual(urljoin(base_url_1, path_2), expected_result)
        self.assertEqual(urljoin(base_url_2, path_1), expected_result)
        self.assertEqual(urljoin(base_url_2, path_2), expected_result)

    def test_urljoin_trailing_slash(self):
        base_url_1 = "https://jovian.ml"
        base_url_2 = "https://jovian.ml/"

        path_1 = "user/siddhant/"
        path_2 = "/user/siddhant/"

        expected_result = "https://jovian.ml/user/siddhant/"

        self.assertEqual(urljoin(base_url_1, path_1), expected_result)
        self.assertEqual(urljoin(base_url_1, path_2), expected_result)
        self.assertEqual(urljoin(base_url_2, path_1), expected_result)
        self.assertEqual(urljoin(base_url_2, path_2), expected_result)

    def test_urljoin_multiple(self):
        base_url_1 = "https://jovian.ml"

        path_1 = "user/siddhant/"
        path_2 = "/gists/starred"

        expected_result = "https://jovian.ml/user/siddhant/gists/starred"

        self.assertEqual(urljoin(base_url_1, path_1, path_2), expected_result)

    def test_urljoin_malformed(self):
        base_url_1 = "https://jovian.ml"
        base_url_2 = "https://jovian.ml/"

        path_1 = "///user/siddhant/"
        path_2 = "//user/siddhant//////"

        expected_result = "https://jovian.ml/user/siddhant/"

        self.assertEqual(urljoin(base_url_1, path_1), expected_result)
        self.assertEqual(urljoin(base_url_1, path_2), expected_result)
        self.assertEqual(urljoin(base_url_2, path_1), expected_result)
        self.assertEqual(urljoin(base_url_2, path_2), expected_result)

    def test_urljoin_no_args(self):
        with self.assertRaises(TypeError) as cm:
            urljoin()

        self.assertEqual(str(cm.exception), "urljoin requires at least one argument")

    def test_urljoin_single_url(self):
        base_url_1 = "https://jovian.ml"
        base_url_2 = "https://jovian.ml/"

        self.assertEqual(urljoin(base_url_1), base_url_1)
        self.assertEqual(urljoin(base_url_2), base_url_2)

    def test_urljoin_single_path(self):
        path_1 = "///user/siddhant"
        path_2 = "//user/siddhant/"

        expected_result = "user/siddhant"

        self.assertEqual(urljoin(path_1), expected_result)
        self.assertEqual(urljoin(path_1), expected_result)


if __name__ == '__main__':
    unittest.main()
