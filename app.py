from flask import Flask, render_template, request
import os
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from rapidfuzz import fuzz

app = Flask(__name__)

DATA_FOLDER = "texts"


# 🔍 Smart match function
def smart_match(query, text):
    return fuzz.partial_ratio(query.lower(), text.lower()) > 60


# 📄 TEXT file search
def search_name(query):
    results = []

    # English → Marathi convert
    marathi_query = transliterate(query, sanscript.ITRANS, sanscript.DEVANAGARI)

    # folder check (important)
    if not os.path.exists(DATA_FOLDER):
        return results

    for file in os.listdir(DATA_FOLDER):
        try:
            with open(os.path.join(DATA_FOLDER, file), encoding="utf-8") as f:
                for line in f:
                    if smart_match(query, line) or smart_match(marathi_query, line):
                        results.append(line.strip())
        except:
            continue

    return results


# 🔥 COMBINED SEARCH (currently only TEXT)
def search_all(query):
    return search_name(query)


# 🌐 MAIN ROUTE
@app.route('/', methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        name = request.form.get("name")
        if name:
            results = search_all(name)

    return render_template("index.html", results=results)


# 🚀 RUN (Render compatible)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
