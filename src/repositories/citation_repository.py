from config import db, EXPORT_FILE_PATH
from sqlalchemy import text

from entities.citation import Citation


def get_citations():
    result = db.session.execute(text("SELECT * FROM citations"))
    citations = result.fetchall()
    return (
        [
            Citation(
                citation.id,
                citation.citation_type,
                "generate_citekey(citation.author, citation.title, citation.year)",
                {
                    field: value
                    for (field, value) in zip(citation._fields[2:], citation[2:])
                    if value != None
                },
            )
            for citation in citations
        ]
    )


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


# Needs more work, need to consider missing author
# Possibly missing year and title too in case of misc?
def generate_citekey(author, title, year):
    # Assuming in the final product that author is "Last_name, First_name Second_name"
    # Example: {Smith, John: This is a book (2019)} = SmithTiab25_2019
    key = ""
    if "," in author:
        author = author.split(",")[0]
    key += author
    if " " in title:
        title = title.split(" ")
    for i in title:
        key += i[0]
    key += str(len(author) + len(title))
    key += "_" + str(year)
    return key


def generate_valid_bibtex_entry(citation):
    bib = f"@{citation.citation_type}{{{citation.citekey},"

    for field in citation.fields:
        bib += f"\n    {field} = {citation.fields[field]},"

    bib = bib[:-1] + "\n}\n\n"

    return bib


def export_all_citations():
    citations = get_citations()

    with open(EXPORT_FILE_PATH, "w", encoding="utf-8") as file:
        write_string = ""
        for citation in citations:
            write_string += generate_valid_bibtex_entry(citation)
        file.write(write_string)

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
            "required": [],
            "optional": ["author", "title", "howpublished", "month", "year", "note"],
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
