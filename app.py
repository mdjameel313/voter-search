from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from rapidfuzz import fuzz
from flask import Flask, render_template, request
import os

app = Flask(__name__)

DATA_FOLDER = "texts"

def smart_match(query, text):
    return fuzz.partial_ratio(query.lower(), text.lower()) > 70


def search_name(query):
    results = []

    # English → Marathi convert
    marathi_query = transliterate(query, sanscript.ITRANS, sanscript.DEVANAGARI)

    for file in os.listdir(DATA_FOLDER):
        with open(os.path.join(DATA_FOLDER, file), encoding="utf-8") as f:
            for line in f:
                if smart_match(query, line) or smart_match(marathi_query, line):
                    results.append(line.strip())

    return results
    results = []
    query = query.lower()

    for file in os.listdir(DATA_FOLDER):
        with open(os.path.join(DATA_FOLDER, file), encoding="utf-8") as f:
            for line in f:
                if query in line.lower():
                    results.append(line.strip())

    return results


@app.route('/', methods=["GET", "POST"])
def home():
    results = []
    if request.method == "POST":
        name = request.form.get("name")
        results = search_all(name)

    return render_template("index.html", results=results)


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
import pdfplumber

def search_pdf(query):
    results = []
    query = query.lower()

    def smart_match(query, text):
    return fuzz.partial_ratio(query.lower(), text.lower()) > 70


def search_name(query):
    results = []

    # English → Marathi convert
    marathi_query = transliterate(query, sanscript.ITRANS, sanscript.DEVANAGARI)

    for file in os.listdir(DATA_FOLDER):
        with open(os.path.join(DATA_FOLDER, file), encoding="utf-8") as f:
            for line in f:
                if smart_match(query, line) or smart_match(marathi_query, line):
                    results.append(line.strip())

    return results
