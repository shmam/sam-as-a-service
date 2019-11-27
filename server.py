from flask import Flask, Response
from spotify_services.service import *
from static_content.render_html import * 
import json
app = Flask(__name__)

@app.route('/' , methods=['GET'])
def hello_world():
    current_track = getMyCurrentPlayback()
    recent_tracks = getMyRecentTracks()
    html = generate_html(current_track, recent_tracks)
    return Response(html, status=200, mimetype='text/html')

@app.route('/api/v1/get_current_track', methods=['GET'])
def get_current_track():
    returning_data = getMyCurrentPlayback()
    return Response(json.dumps(returning_data), status=200, mimetype='application/json')

@app.route('/api/v1/get_past_tracks' , methods=['GET'])
def get_past_track():
    returning_data = {"tracks": getMyRecentTracks()}
    return Response(json.dumps(returning_data), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)