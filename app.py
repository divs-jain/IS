from flask import Flask, render_template, request, jsonify
from pii_module.pipeline import process_text

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    text = data.get("text", "")
    prompt_type = data.get("prompt_type", "reasoning")
    result = process_text(text, prompt_type=prompt_type)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
