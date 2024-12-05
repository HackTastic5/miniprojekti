import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

test_env = os.getenv("TEST_ENV") == "true"
#api_env = os.getenv("API_KEY") == "true"
print(f"Test environment: {test_env}")
model = genai.GenerativeModel("gemini-1.5-flash")

# dirname = os.path.dirname(__file__)
# EXPORT_FILE_NAME = "citations.bib"
# EXPORT_FILE_PATH = os.path.join(dirname, "..", "data", EXPORT_FILE_NAME)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)
