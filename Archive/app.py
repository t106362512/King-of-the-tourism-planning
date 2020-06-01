from flask import Flask, jsonify, escape, request
import json
import yfinance as yf


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False

@app.route('/', methods=['GET', 'POST'])
def home():
    request_json = request.get_json(silent=True)
    request_args = request.args
    ELEMENT = ['stockName', 'start', 'end']
    try:
        if len(request_args) != 0:
            stockName = request_args.get('stockName')
            start = request_args.get('start')
            end = request_args.get('end')

        elif len(request_json) != 0:
            stockName = request_json['stockName']
            start = request_json['start']
            end = request_json['end']
        
        else:
            return 'U need give me the {}!'.format(escape(', '.join(ELEMENT)))
        return jsonify(json.loads(yf.download(stockName, start=start, end=end, group_by="ticker").to_json(date_unit="s", date_format='iso')))
        # return jsonify(yf.download(stockName, start=start, end=end, group_by="ticker").reset_index().df['Date'].to_dict())
    except Exception as e:
        return '{}'.format(repr(e))

app.run()