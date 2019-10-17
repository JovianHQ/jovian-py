import unittest

from jovian.utils.url import urljoin


class UrlUtilsTest(unittest.TestCase):

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
