from flask import escape, jsonify, Response, app, make_response
# from flask_api import status
import yfinance as yf
import json

def ntut_http_triger(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    INPUT_OBJ = ['stockName', 'start', 'end']

    try:
        if len(request.args) != 0  or request.get_json(silent=True) is not None:
            my_request = request.get_json() if request.get_json(silent=True) is not None else request.args
            if all(ELEMENT in my_request for ELEMENT in INPUT_OBJ):
                stockName = my_request['stockName']
                start = my_request['start']
                end = my_request['end']
            else:
                return jsonify({'error': 'U need give me the {}!'.format(', '.join(INPUT_OBJ))}), 400
        else:
            return jsonify({'error': 'U need give me the {}!'.format(', '.join(INPUT_OBJ))}), 400
        return jsonify(json.loads(yf.download(stockName, start=start, end=end, group_by="ticker").to_json(date_unit="s", date_format='iso'))), 200
    except Exception as e:
        return jsonify({'error': f'{repr(e)}'}), 500