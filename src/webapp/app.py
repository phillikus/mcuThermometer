#!flask/bin/python
from flask import Flask
from flask_cors import CORS
import redis
import flask

app = Flask(__name__, static_url_path='')
CORS(app)

red = redis.StrictRedis()

def therm_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('therm')

    for message in pubsub.listen():
        if isinstance(message['data'], (bytes, bytearray)):
            result = message['data'].decode('utf-8')
            yield 'data: %s\n\n' % result

@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/push', methods=['POST'])
def post():
    message = flask.request.data
    red.publish('therm', message)
    return flask.Response(status=204)


@app.route('/stream')
def stream():
    return flask.Response(therm_stream(), mimetype="text/event-stream")



if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.35')
