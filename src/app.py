from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.citation_repository import (
    get_citations,
    create_citation,
    get_citation_types,
)
from config import app, test_env


@app.route("/", methods=["GET", "POST"])
def index():
    citations = get_citations()
    all_citation_types = get_citation_types()
    citation_type = None

    if request.method == "POST":
        citation_type = request.form["citation_type"]
    return render_template(
        "index.html",
        citations=citations,
        citation_type=citation_type,
        all_citation_types=all_citation_types,
    )


@app.route("/create_citation", methods=["POST"])
def citation_creation():
    citation_type = request.form.get("citation_type")
    author = request.form.get("author")
    title = request.form.get("title")
    year = request.form.get("year")
    print(citation_type, author, title, year)

    try:
        create_citation(citation_type, author, title, year)
        return redirect("/")
    except Exception as error:
        print(error)
        flash(str(error))
        return redirect("/")


# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
