class Citation:
    def __init__(self, id, citation_type, citekey, fields):
        self.id = id
        self.citation_type = citation_type
        self.citekey = citekey
        self.fields = fields

    def __str__(self):
        return f"{self.fields.get('title')} by {self.fields.get('author')} {{{self.citekey}}}"
