from flask import Flask, render_template, request
import os
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from rapidfuzz import fuzz

app = Flask(__name__)
TEXT_FOLDER = "texts"

def search_name(keyword):
    results = []
    for file in os.listdir(TEXT_FOLDER):
        if file.endswith(".txt"):
            path = os.path.join(TEXT_FOLDER, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for i, line in enumerate(f):
                    score = fuzz.partial_ratio(keyword, line)
                    if score > 70:   # fuzzy match
                        results.append({
                            "file": file,
                            "line": i+1,
                            "text": line.strip()
                        })
    return results

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        name = request.form["name"]

        marathi_name = transliterate(name, sanscript.ITRANS, sanscript.DEVANAGARI)

        results = search_name(marathi_name) + search_name(name)

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
