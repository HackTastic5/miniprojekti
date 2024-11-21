import unittest
from util import validate_field, UserInputError

class TestCitations(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_author_does_not_raise_error(self):
        validate_field("author", "Author", min_len=5, max_len=40)

    def test_invalid_author_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_field("author", "Au", min_len=5, max_len=40)

        with self.assertRaises(UserInputError):
            validate_field("author", "Author" * 10, min_len=5, max_len=40)

    def test_valid_year_does_not_raise_error(self):
        validate_field("year", "2024", exact_len=4)

    def test_invalid_year_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_field("year", "24", exact_len=4)
