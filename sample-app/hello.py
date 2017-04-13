import datetime

from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World! {}".format(datetime.utcnow())


@app.route("/health/")
def health():
    return "98.6"


if __name__ == "__main__":
    app.run(port=80, host='0.0.0.0')
