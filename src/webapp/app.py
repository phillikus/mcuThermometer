#!flask/bin/python
from flask import Flask
from flask_cors import CORS

from controllers.therm import therm_controller

app = Flask(__name__, static_url_path='')
app.register_blueprint(therm_controller)
CORS(app)


@app.route('/')
def root():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
