from flask import Flask
from flask import url_for

app = Flask(__name__)


@app.route('/')
def hello_world():
    return url_for('static', filename='stat.html')

if __name__ == '__main__':
    app.run()
