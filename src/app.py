from io import BytesIO
from flask import redirect, render_template, request, jsonify, flash, send_file
import pathvalidate
from db_helper import reset_db
from repositories.citation_repository import (
    get_citations,
    create_citation,
    get_citation_types,
    delete_citation,
    update_citation,
    export_all_citations,
    get_citation_by_doi,
)
from config import app, test_env, model
from util import validate_field, UserInputError


@app.route("/", methods=["GET", "POST"])
def index():
    citations = get_citations()
    all_citation_types = get_citation_types()
    citation_type = None
    fields = {}
    editing_id = -1

    if request.method == "POST":
        citation_type = request.form.get("citation_type")
        editing_id = int(request.form.get("editing_id") or -1)
        doi = request.form.get("doi")
        if doi:
            doi_result = get_citation_by_doi(doi)
            if doi_result:
                citation_type = doi_result["citation_type"]
                fields = doi_result["fields"]
            else:
                flash("No results found for specified DOI")

    return render_template(
        "index.html",
        citations=citations,
        citation_type=citation_type,
        fields=fields,
        editing_id=editing_id,
        all_citation_types=all_citation_types,
    )


@app.route("/ai", methods=["GET", "POST"])
def helper():
    citation_type = None
    fields = {}
    all_citation_types = get_citation_types()
    ##counter=0

    if request.method == "POST":
        prompt = request.form.get("ai_prompt")
        print(prompt)
        response = model.generate_content(
            f"Give any DOI number for an article that is related to {prompt}, "
            f"give me just the doi number and nothing else"
        )
        print(response.text)
        doi_result = get_citation_by_doi(response.text)
        print(doi_result)
        if doi_result:
            citation_type = doi_result["citation_type"]
            fields = doi_result["fields"]

    return render_template(
        "ai.html",
        citation_type=citation_type,
        fields=fields,
        all_citation_types=all_citation_types,
    )


@app.route("/create_citation", methods=["POST"])
def citation_creation():
    citation_type = request.form.get("citation_type")
    ##author = request.form.get("author")
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

    except UserInputError as error:
        print(error)
        flash(str(error))
        return redirect("/")


@app.route("/delete_citation", methods=["POST"])
def citation_deletion():
    citation_id = request.form.get("citation_id")
    delete_citation(citation_id)

    return redirect("/")


@app.route("/update_citation", methods=["POST"])
def edit_citation():
    update_citation(request.form.to_dict())

    return redirect("/")


@app.route("/view_bibtex", methods=["GET"])
def view_bibtex():
    return redirect("/")


@app.route("/export_citations", methods=["POST"])
def export_citations():
    bibname = request.form.get("bibname") + ".bib"
    bibtex = export_all_citations()

    try:
        pathvalidate.validate_filename(bibname)
    except pathvalidate.error.ValidationError as error1:
        # Still shows the successful alert for now
        print(error1)
        flash(str(error1))
        return redirect("/")

    bibfile = BytesIO()
    bibfile.write(bibtex.encode("utf-8"))
    bibfile.seek(0)

    return send_file(
        bibfile,
        download_name=bibname,
        mimetype="application/x-bibtex",
        as_attachment=True,
    )


# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})

    @app.route("/review_data")
    def create_review_data():
        create_citation(
            "article",
            {
                "author": "Zimmerman, Barry J",
                "title": "Becoming a self-regulated learner: An overview",
                "year": "2002",
                "journal": "Theory into practice",
                "volume": "41",
                "number": "2",
                "pages": "64--70",
                "publisher": "Taylor & Francis",
            },
        )

        create_citation(
            "article",
            {
                "title": "Procrastination at work and time management training",
                "author": "Eerde, Wendelien Van",
                "journal": "The Journal of psychology",
                "volume": "137",
                "number": "5",
                "pages": "421--434",
                "year": "2003",
                "publisher": "Taylor & Francis",
            },
        )

        create_citation(
            "inproceedings",
            {
                "title": (
                    "Examining the role of self-regulated "
                    "learning on introductory programming performance"
                ),
                "author": "Bergin, Susan and Reilly, Ronan and Traynor, Desmond",
                "booktitle": (
                    "Proceedings of the first international workshop "
                    "on Computing education research"
                ),
                "pages": "81--86",
                "year": "2005",
            },
        )
        return redirect("/")
