from flask import Flask, current_app

app = Flask(__name__)

@app.route('/')
def hello_world():
    return current_app.send_static_file('stat.html')


if __name__ == '__main__':
    app.run()
