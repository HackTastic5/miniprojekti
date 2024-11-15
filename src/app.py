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
    title = request.form.get("title")
    print(author, title)

    try:
        create_citation(author, title)
        return redirect("/")
    except Exception as error:
        print(error)
        flash(str(error))
        return  redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
