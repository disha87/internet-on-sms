from flask import Flask, request
import twilio.twiml
import requests
import googlemaps
import json
import re

app = Flask(__name__)

ERROR = "Could not find route, Please enter route " +\
    "as From: <Intersection> To: <Intersection>"

google_client = googlemaps.Client('AIzaSyDrOaGEwofGZi6uilv5fhhimrJT-BKCzJE')


def get_geocode(address):
    try:
        out = google_client.geocode(address)[0]['geometry']['location']
    except:
        return ERROR
    return str(out['lat']) + '%2C' + str(out['lng'])


def pretty_output(directions):
    count = 1
    out = ''
    for item in directions:
        out += 'Step ' + str(count) + ': '
        out += item
        out += '\n'
    count += 1
    return out


def parse_output(text):
    out = json.loads(text)
    maneuver = out['response']['route'][0]['leg'][0]['maneuver']
    directions = []
    for item in maneuver:
        directions.append(re.sub('<[^<]+?>', '', item['instruction']))
    return pretty_output(directions)


def get_response_from_here(msg):
    from_m = re.search(r'From:(.*)To:(.*)', msg).group(1)
    to_m = re.search(r'From:(.*)To:(.*)', msg).group(2)
    from_g = get_geocode(from_m)
    to_g = get_geocode(to_m)
    if from_g == ERROR or to_g == ERROR:
        return ERROR

    url = 'https://route.cit.api.here.com/routing/7.2/calculateroute.json' +\
        '?waypoint0=' + from_g + \
        '&waypoint1=' + to_g + \
        '&mode=fastest%3Bcar%3Btraffic%3Aenabled' + \
        '&app_id=xY0izChQ6ho5GyDaxgoA' + \
        '&app_code=UVZwg2O6QS1cZwTmdjldqw&departure=now'

    try:
        r = requests.get(url)
        return parse_output(r.text)
    except:
        return "Service is down, please try again later"


@app.route("/", methods=['GET', 'POST'])
def get_route():
    """Respond to incoming calls with a simple text message."""
    resp = twilio.twiml.Response()
    try:
        body = request.values.get('Body', '')
        msg = get_response_from_here(body)
        resp.message(msg)
    except:
        resp.message(ERROR)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
