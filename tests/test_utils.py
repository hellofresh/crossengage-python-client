import unittest

from crossengage.utils import update_dict


class TestUtils(unittest.TestCase):

    def test_update_dict(self):
        old_dict = dict(a=1, b=2)

        new_dict = update_dict(old_dict, dict(a=2, b=3, c=4))

        self.assertEqual(dict(a=1, b=2), old_dict)
        self.assertEqual(dict(a=2, b=3, c=4), new_dict)
