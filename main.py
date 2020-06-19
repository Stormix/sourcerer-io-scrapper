from datetime import date

from dotenv import load_dotenv
from flask import Flask, abort, jsonify, make_response, request, send_file
from flask.json import JSONEncoder

from src import Sourcerer

load_dotenv()


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder


@app.route('/')
def index():
    return make_response("OK", 200)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/fetch/<string:username>')
def getInfo(username):
    if not username:
        return make_response("Missing username", 422)
    try:
        scrapper = Sourcerer(username)
        scrapper.launchBrowser()
        scrapper.fillInfo()
        scrapper.browser.close()
        
        return scrapper.data
    except:
        return make_response("Something went wrong ¯\_(ツ)_/¯", 418)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
