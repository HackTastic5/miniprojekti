class Citation:
    def __init__(self, id, author, title):
        self.id = id
        self.author = author
        self.title = title

    def __str__(self):
        return f"{self.title} by {self.author}"
