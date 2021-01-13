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

cache = dict()

@app.route('/', methods=['POST'])
@cross_origin()
def home():
    if 'id' in request.json:
        id = request.json['id']
    else:
        return "Error: No id field provided. Please specify an id."

    try:
        with open(id + '.json') as json_file:
            data = json.load(json_file)
        
        if data:
            print(data)
            return jsonify(data)
    except:
        print('nothing found')

    if cache.get(id):
        response = {}
        response['error'] = 1000
        response['message'] = cache.get(id)
        return jsonify(response), 400
    else:
        cache[id] = True

    # Create an empty list for our results
    scraped_results = scrape(id, debug = False)

    results = parse(scraped_results, cache, id)

    with open(id + '.json', 'w') as json_file:
        json.dump(results, json_file, cls=MyEncoder)

    cache[id] = False
    return MyEncoder().encode(results)

app.run(host='0.0.0.0')
