from config import db
from sqlalchemy import text
from util import validate_citation

from entities.citation import Citation


def get_citations():
    result = db.session.execute(text("SELECT * FROM citations"))
    citations = result.fetchall()
    return [
        Citation(
            citation.id,
            citation.citation_type,
            citation.author,
            citation.title,
            citation.booktitle,
            citation.year,
        )
        for citation in citations
    ]


def create_citation(citation_type, author, title, booktitle, year):
    sql = text(
        "INSERT INTO citations"
        "(citation_type, author, title, booktitle, year)"
        "VALUES"
        "(:citation_type, :author, :title, :booktitle, :year)"
    )
    db.session.execute(
        sql,
        {
            "citation_type": citation_type,
            "author": author,
            "title": title,
            "booktitle": booktitle,
            "year": year,
        },
    )
    db.session.commit()


# This has to be relocated
def get_citation_types():
    citation_types = {
        "article": {
            "required": ["author", "title", "year", "journal"],
            "optional": ["volume", "number", "pages", "month", "note"],
        },
        "book": {
            "required": ["author", "editor", "title", "publisher", "year"],
            "optional": [
                "volume",
                "number",
                "series",
                "address",
                "edition",
                "month",
                "note",
            ],
        },
        "booklet": {
            "required": ["title", "author", "howpublished", "address", "year"],
            "optional": [
                "editor",
                "volume",
                "number",
                "series",
                "organization",
                "month",
                "note",
            ],
        },
        "conference": {
            "required": ["author", "title", "booktitle", "year"],
            "optional": [
                "editor",
                "volume",
                "number",
                "series",
                "pages",
                "address",
                "month",
                "organization",
                "publisher",
                "note",
            ],
        },
        "inbook": {
            "required": ["author", "title", "booktitle", "publisher", "year"],
            "optional": [
                "editor",
                "volume",
                "number",
                "series",
                "address",
                "edition",
                "month",
                "pages",
                "note",
            ],
        },
        "incollection": {
            "required": ["author", "title", "booktitle", "publisher", "year"],
            "optional": [
                "editor",
                "volume",
                "number",
                "series",
                "pages",
                "address",
                "month",
            ],
        },
        "inproceedings": {
            "required": ["author", "title", "booktitle", "year"],
            "optional": [
                "editor",
                "volume",
                "number",
                "series",
                "pages",
                "address",
                "month",
                "organization",
                "note",
            ],
        },
        "manual": {
            "required": ["title", "year"],
            "optional": [
                "author",
                "organization",
                "address",
                "edition",
                "month",
                "note",
            ],
        },
        "mastersthesis": {
            "required": ["author", "title", "school", "year"],
            "optional": ["type", "address", "month", "note"],
        },
        "misc": {"required": [], "optional": []},
        "phdthesis": {
            "required": ["author", "title", "school", "year"],
            "optional": ["type", "address", "month", "note"],
        },
        "proceedings": {
            "required": ["title", "year"],
            "optional": [
                "editor",
                "volume",
                "number",
                "series",
                "address",
                "month",
                "publisher",
            ],
        },
        "techreport": {
            "required": ["author", "title", "institution", "year"],
            "optional": ["type", "number", "address", "month", "note"],
        },
        "unpublished": {
            "required": ["author", "title", "note"],
            "optional": ["month", "year"],
        },
    }
    return citation_types
