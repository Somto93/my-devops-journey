from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Somto's DevOps Networking Lab</h1>
    <p>Application is running successfully.</p>
    """

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
