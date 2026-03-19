from flask import Flask, render_template, request
import os
import pdfplumber
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from rapidfuzz import fuzz

app = Flask(__name__)

DATA_FOLDER = "texts"
PDF_FOLDER = "pdfs"


# 🔍 Smart match function
def smart_match(query, text):
    return fuzz.partial_ratio(query.lower(), text.lower()) > 60


# 📄 TEXT file search
def search_name(query):
    results = []
    marathi_query = transliterate(query, sanscript.ITRANS, sanscript.DEVANAGARI)

    for file in os.listdir(DATA_FOLDER):
        with open(os.path.join(DATA_FOLDER, file), encoding="utf-8") as f:
            for line in f:
                if smart_match(query, line) or smart_match(marathi_query, line):
                    results.append(line.strip())

    return results


# 📑 PDF search (line by line)
def search_pdf(query):
    results = []
    marathi_query = transliterate(query, sanscript.ITRANS, sanscript.DEVANAGARI)

    for file in os.listdir(PDF_FOLDER):
        if file.endswith(".pdf"):
            with pdfplumber.open(os.path.join(PDF_FOLDER, file)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        lines = text.split("\n")

                        for line in lines:
                            if smart_match(query, line) or smart_match(marathi_query, line):
                                results.append(f"{file}: {line.strip()}")

    return results


# 🔥 COMBINED SEARCH
def search_all(query):
    results = []
    results += search_name(query)
    results += search_pdf(query)
    return results


# 🌐 MAIN ROUTE
@app.route('/', methods=["GET", "POST"])
def home():
    results = []
    if request.method == "POST":
        name = request.form.get("name")
        results = search_all(name)

    return render_template("index.html", results=results)


# 🚀 RUN
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
