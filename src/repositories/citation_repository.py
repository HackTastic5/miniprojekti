from config import db
from sqlalchemy import text
from util import validate_citation

from entities.citation import Citation

def get_citations():
    result = db.session.execute(text("SELECT id, author, title FROM citations"))
    citations = result.fetchall()
    return [Citation(citation[0], citation[1], citation[2]) for citation in citations] 

def create_citation(author, title):
    sql = text("INSERT INTO citations (author, title) VALUES (:author, :title)")
    db.session.execute(sql, {"author": author, "title": title })
    db.session.commit()
