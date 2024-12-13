import unicodedata
import requests
import bibtexparser
from sqlalchemy import text
from config import db

from entities.citation import Citation


def get_citations(sort=None, desc=False):
    order = "DESC" if desc else "ASC"

    match sort:
        case "author":
            sortkey = f"author {order}"
        case "title":
            sortkey = f"title {order}"
        case "date":
            sortkey = f"year::int {order}"
        case _:
            sortkey = f"id {order}"

    result = db.session.execute(text(f"SELECT * FROM citations ORDER BY {sortkey}"))
    citations = result.fetchall()
    return [
        Citation(
            citation.id,
            citation.citation_type,
            generate_citekey(
                citation.author, citation.title, citation.year, citation.id
            ),
            {
                field: value
                for (field, value) in zip(citation._fields[2:], citation[2:])
                if value is not None
            },
        )
        for citation in citations
    ]


def create_citation(citation_type, fields):
    fields.update({"citation_type": citation_type})

    sql = text(
        "INSERT INTO citations"
        f"({', '.join(key for key in fields.keys())})"
        "VALUES"
        f"({', '.join(f':{key}' for key in fields.keys())})"
    )
    db.session.execute(
        sql,
        fields,
    )

    print(fields)
    db.session.commit()


# A null author is left out of the final key
# Title and year have NOT NULL constraints
# but if that changes this will have to be reworked
def generate_citekey(author, title, year, cite_id):
    # Assuming in the final product that author is "Last_name, First_name Second_name"
    # Example: {Smith, John: This is a book (2019)} and id 25 = SmithThis25_2019
    key = ""

    if author is not None:
        if "," in author:
            author = author.split(",")[0]
        key += author.replace(
            " ", ""
        )  # also works if the author is in format first_name last_name

    title_part_len = 20
    first_whitespace_index = title.find(" ", 0, title_part_len)
    if first_whitespace_index != -1:
        key += "".join(
            c
            for c in title[:first_whitespace_index]
            if unicodedata.category(c).startswith("L")
        )
    else:
        key += "".join(
            c for c in title[:title_part_len] if unicodedata.category(c).startswith("L")
        )

    key += str(year)
    key += "_" + str(cite_id)  # uses the citation id to ensure uniqueness
    return key


def generate_valid_bibtex_entry(citation):
    bib = f"@{citation.citation_type}{{{citation.citekey},"

    for field in citation.fields:
        bib += f"\n    {field} = {{{citation.fields[field]}}},"

    bib = bib[:-1] + "\n}\n\n"

    return bib


def get_citation_by_doi(doi):
    url = f"https://doi.org/{doi}"
    headers = {"accept": "application/x-bibtex"}

    response = requests.get(url, headers=headers, timeout=15)
    content_type = response.headers["content-type"]
    if response.status_code == 200 and content_type == "application/x-bibtex":
        bibtex_entry = response.text.strip()
        try:
            parsed_entry = bibtexparser.parse_string(bibtex_entry).entries[0]
        except IndexError:
            return None
        fields = {field.key: field.value for field in parsed_entry.fields}

        return {"citation_type": parsed_entry.entry_type, "fields": fields}

    return None


def export_all_citations():
    citations = get_citations()

    write_string = ""
    for citation in citations:
        write_string += generate_valid_bibtex_entry(citation)

    return write_string


def update_citation(data):
    fields_to_update = list(data.keys())
    fields_to_update.remove("citation_id")
    for key, value in data.items():
        if value == "":
            data[key] = None

    sql = text(
        "UPDATE citations "
        f"SET {', '.join(f'{key}=:{key}' for key in fields_to_update)} "
        "WHERE id=:citation_id;"
    )
    db.session.execute(sql, data)
    db.session.commit()


def delete_citation(id):
    sql = text("DELETE FROM citations WHERE id=:id;")
    db.session.execute(sql, {"id": id})
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
        "misc": {
            "required": ["title", "year"],
            "optional": ["author", "howpublished", "month", "note"],
        },
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
