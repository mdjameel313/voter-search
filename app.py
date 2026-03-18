from flask import Flask, render_template, request
import os

app = Flask(__name__)

DATA_FOLDER = "texts"

def search_name(query):
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
        results = search_name(name)

    return render_template("index.html", results=results)


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
