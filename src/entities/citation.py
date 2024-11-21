class Citation:
    def __init__(self, id, citation_type, author, title, booktitle, year):
        self.id = id
        self.citation_type = citation_type
        self.author = author
        self.title = title
        self.booktitle = booktitle
        self.year = year

    def __str__(self):
        return f"{self.title} by {self.author}"
