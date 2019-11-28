def generate_html(current_track_obj, past_track_list): 
    html_string_head = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>Sam-as-a-service</title>
        <meta name="author" content="">
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>body {font-family: Arial,Helvetica Neue,Helvetica,sans-serif;}</style>
        </head> 
        <body>  
        <h1><u>Sam as a Service</u> ⚡️</h1> """

    if current_track_obj == "user is not playing any tracks":
        html_string_current_playing = "<p>Sam is not currently playing any music on spotify </p>"
    else: 
        html_string_current_playing= """
            <p> Sam is currently listening to <strong>{0}</strong> by <strong>{1}</strong> </p>
            <iframe src="https://open.spotify.com/embed/track/{2}" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
            """.format(current_track_obj["track_name"], current_track_obj["artists_name"], current_track_obj["track_id"])

    html_string_past = """
        <br>
        <br>
        <h4> Most Recently Played Tracks </h4>
        <ul>"""

    for i in range(0,5): 
        html_string_past += """<li><a href="{0}">{1}</a> by {2}</li>""".format(past_track_list[i]["track_external_url"], past_track_list[i]["track_name"], past_track_list[i]["artists_name"])
    html_string_past += "</ul>"

    html_string_ending = """    
        <h4> API endpoints </h4>
        <ul> 
        <li><strong> <a href="/api/v1/current_track"> .../api/v1/current_track </a> </strong>: current track</li>
        <li><strong> <a href="/api/v1/past_tracks"> .../api/v1/past_tracks </a> </strong>: past 20 tracks </li>
        </ul>
        </body>
        </html>"""
    return html_string_head + html_string_current_playing + html_string_past + html_string_ending