from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.citation_repository import (
    get_citations,
    create_citation,
    get_citation_types,
    delete_citation,
    export_all_citations,
)
from config import app, test_env
from util import validate_field


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
    year = request.form.get("year")
    fields = {}

    # Read the required fields
    for key in get_citation_types()[citation_type]["required"]:
        value = request.form.get(key)
        fields[key] = value

    # Read the optional fields that exist
    for key in get_citation_types()[citation_type]["optional"]:
        value = request.form.get(key)
        if len(value) > 0:
            fields[key] = value

    try:
        ##validate_field("author", author, min_len=5, max_len=40)
        validate_field("year", year, exact_len=4)
        create_citation(citation_type, fields)
        return redirect("/")
    except Exception as error:
        print(error)
        flash(str(error))
        return redirect("/")


@app.route("/delete_citation", methods=["POST"])
def citation_deletion():
    citation_id = request.form.get("citation_id")
    delete_citation(citation_id)

    return redirect("/")



@app.route("/export_citations", methods=["POST"])
def export_citations():
    export_all_citations()
    return redirect("/")


# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
