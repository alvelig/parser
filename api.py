import json
import flask
from flask import jsonify, request, Response
from flask_cors import CORS, cross_origin

from scraper import scrape
from parser import parse

from json import JSONEncoder
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

@app.route('/', methods=['POST'])
@cross_origin()
def home():
    if 'id' in request.json:
        id = request.json['id']
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    scraped_results = scrape(id, debug = False)
    results = parse(scraped_results)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return MyEncoder().encode(results)

app.run()
