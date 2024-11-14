from config import db
from sqlalchemy import text

from entities.citation import Citation

def get_citations():
    result = db.session.execute(text("SELECT id, author, name FROM citations"))
    citations = result.fetchall()
    return [Citation(citation[0], citation[1], citation[2]) for citation in citations] 

def create_citation(author, name):
    sql = text("INSERT INTO citations (author, name) VALUES (:author, :name)")
    db.session.execute(sql, {"author": author, "name": name })
    db.session.commit()
