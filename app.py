from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Benvenuto su Fanta Formula 1! 🚦🏎️"

if __name__ == "__main__":
    # Importante: host 0.0.0.0 per Render, porta 10000
    app.run(host="0.0.0.0", port=10000, debug=False)
