import unicodedata

class UserInputError(Exception):
    pass


def validate_field(field, value, min_len=None, max_len=None, exact_len=None):
    if not value:
        raise UserInputError(f"{field} can not be empty")

    if min_len and len(value) < min_len:
        raise UserInputError(f"{field} length must be greater than {min_len}")

    if max_len and len(value) > max_len:
        raise UserInputError(f"{field} length must be smaller than {max_len}")

    if exact_len and len(value) != exact_len:
        raise UserInputError(f"{field} length must be {exact_len}")


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
