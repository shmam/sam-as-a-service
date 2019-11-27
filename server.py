from flask import Flask, Response
from spotify_services.service import *
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return Response('Hello, World!', status=200, mimetype='application/json')

@app.route('/current_track')
def get_current_track():
    return Response(json.dumps(getMyCurrentPlayback()), status=200, mimetype='application/json')

@app.route('/past_track')
def get_past_track():
    return Response(json.dumps({"tracks": getMyRecentTracks()}), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)