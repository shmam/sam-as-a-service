def generate_html(current_track_obj, past_track_list): 
    print(current_track_obj["track_name"], current_track_obj["artists_name"], current_track_obj["track_id"])
    html_string = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>Sam-as-a-service</title>
        <meta name="author" content="">
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>body {{font-family: Arial,Helvetica Neue,Helvetica,sans-serif;}}</style>
        </head>
        <body>
        <h1>Sam as a Service</h1>
        <p> Sam is currently listening to <strong>{0}</strong> by <strong>{1}</strong> </p>
        <iframe src="https://open.spotify.com/embed/track/{2}" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
        </body>
        </html>""".format(current_track_obj["track_name"], current_track_obj["artists_name"], current_track_obj["track_id"])
    return html_string