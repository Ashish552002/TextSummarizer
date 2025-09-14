from flask import Flask, render_template, request
from summarizer import analyze_article

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary, topic, crux, input_text = "", "", "", ""

    if request.method == "POST":
        input_text = request.form["article"]
        if input_text.strip():
            result = analyze_article(input_text, max_sentences=3)
            summary = result["summary"]
            topic = result["topic"]
            crux = result["crux"]

    return render_template("index.html", summary=summary, topic=topic, crux=crux, input_text=input_text)

if __name__ == "__main__":
    app.run(debug=True)
