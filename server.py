from flask import Flask, request, jsonify
from api import AlphaVantageAPI
import json

def get_key():
    """
    Retrieves API key from a JSON file

    Returns:
        str: The API key
    """
    with open('keys.json', 'r') as f:
        data = json.load(f)
    return data['API_KEY']

api = AlphaVantageAPI(
    api_key=get_key(),
    cache_dir='cache'
)
app = Flask(__name__)

@app.route('/lookup', methods=['GET'])
def symbol_lookup():
    """
    Retrieves data for specific symbol and date

    Returns:
        dict: Data for specified symbol and date
    """
    symbol = request.args.get('symbol').upper()
    date = request.args.get('date')

    data = api.get_lookup(symbol, date)
    return jsonify(data)


@app.route('/min', methods=['GET'])
def min():
    """
    Retrieves minimum price among first n data points for a symbol

    Returns:
        dict: Dictionary containing minimum price
    """
    symbol = request.args.get('symbol').upper()
    n = request.args.get('n')

    try:
        n = int(n)
    except:
        return {'Error': 'n must be an integer'}

    return api.get_min(symbol, n)


@app.route('/max', methods=['GET'])
def max():
    """
    Retrieves maximum price among first n data points for a symbol

    Returns:
        dict: Dictionary containing maximum price
    """
    symbol = request.args.get('symbol').upper()
    n = request.args.get('n')
    try:
        n = int(n)
    except:
        return {'Error': 'n must be an integer'}

    return api.get_max(symbol, n)


if __name__ == '__main__':
    app.run(debug=True)
