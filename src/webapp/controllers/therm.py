from flask import Flask, Blueprint, request, jsonify
import flask
import redis

red = redis.StrictRedis()
therm_controller = Blueprint('therm', 'therm', url_prefix='/therm')


def therm_stream():
    pub_sub = red.pubsub()
    pub_sub.subscribe('therm')

    for message in pub_sub.listen():
        if isinstance(message['data'], (bytes, bytearray)):
            result = message['data'].decode('utf-8')
            yield 'data: %s\n\n' % result


@therm_controller.route('/push', methods=['POST'])
def post():
    message = flask.request.data
    red.publish('therm', message)
    return flask.Response(status=204)


@therm_controller.route('/stream')
def stream():
    return flask.Response(therm_stream(), mimetype="text/event-stream")
