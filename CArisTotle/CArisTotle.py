from flask import Flask, current_app

app = Flask('CArisTotle')


@app.route('/')
def hello_world():
    # return url_for('static', filename='stat.html')
    return current_app.send_static_file('stat.html')

if __name__ == '__main__':
    app.run()
