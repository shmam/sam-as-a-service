from flask import Flask, Response, send_file
from spotify_services.service import *
from static_content.render_html import * 
from static_content.render_error import *
import json
app = Flask(__name__)

@app.route('/' , methods=['GET'])
def hello_world():
    try: 
        current_track = getMyCurrentPlayback()
        recent_tracks = getMyRecentTracks()
        returning_data = recent_tracks_audio_features(getMyRecentTracks())
        generateRadarChart(returning_data)
        html = generate_html(current_track, recent_tracks)
        return Response(html, status=200, mimetype='text/html')
    except Exception as err: 
        html = generate_error_html(err)
        return Response(html, status=500, mimetype='text/html')

@app.route('/api/v1/current_track', methods=['GET'])
def get_current_track():
    returning_data = getMyCurrentPlayback()
    return Response(json.dumps(returning_data), status=200, mimetype='application/json')

@app.route('/api/v1/past_tracks' , methods=['GET'])
def get_past_track():
    returning_data = {"tracks": getMyRecentTracks()}
    return Response(json.dumps(returning_data), status=200, mimetype='application/json')

@app.route('/api/v1/past_tracks/analyze' , methods=['GET'])
def analyze_past_track():
    returning_data = recent_tracks_audio_features(getMyRecentTracks())
    return Response(json.dumps(returning_data), status=200, mimetype='application/json')

@app.route('/api/v1/past_tracks/analyze/img.png' , methods=['GET'])
def analyze_past_track_img():
    returning_data = recent_tracks_audio_features(getMyRecentTracks())
    generateRadarChart(returning_data)
    return send_file("img.png", mimetype='image/gif')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)