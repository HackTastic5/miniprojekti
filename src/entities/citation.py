class Citation:
    def __init__(self, id, author, name):
        self.id = id
        self.author = author
        self.name = name

    def __str__(self):
        return f"{self.name} by {self.author}"
