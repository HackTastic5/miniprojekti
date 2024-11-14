from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.citation_repository import get_citations, create_citation
from config import app, test_env

@app.route("/")
def index():
    citations = get_citations()
    return render_template("index.html", citations=citations) 



@app.route("/create_citation", methods=["POST"])
def citation_creation():
    author = request.form.get("author")
    name = request.form.get("name")

    try:
        create_citation(author, name)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return  redirect("/new_citation")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
