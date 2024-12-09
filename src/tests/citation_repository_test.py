import unittest
from repositories import citation_repository
from entities.citation import Citation


class TestCitationRepository(unittest.TestCase):
    def setUp(self):
        pass

    def test_generate_citekey_uses_author_title_year_id(self):
        citekey = citation_repository.generate_citekey("Author", "Title", "2024", 1)

        self.assertEqual(citekey, "AuthorTitle2024_1")

    def test_generate_citekey_multiword_title_only_first_letters(self):
        citekey = citation_repository.generate_citekey(
            "Author", "Title of Source", "2024", 1
        )

        self.assertEqual(citekey, "AuthorTitle2024_1")

    def test_generate_bibtex_entry_generates_valid_bibtex(self):
        fields = {
            "author": "Author",
            "title": "Title",
            "year": "2024",
            "journal": "Journal",
        }
        citation = Citation(1, "article", "AuthorTitle2024_1", fields)

        tested_bibtex = citation_repository.generate_valid_bibtex_entry(citation)

        good_bibtex = (
            "@article{AuthorTitle2024_1,\n"
            "    author = {Author},\n    title = {Title},\n"
            "    year = {2024},\n    journal = {Journal}\n}\n\n"
        )

        self.assertEqual(tested_bibtex, good_bibtex)
