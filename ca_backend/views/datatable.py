from flask import Blueprint, render_template, g, session, request, jsonify
from models.model import BaseDataTables
import os
import json

datable = Blueprint('datable', __name__, template_folder='templates',
                    static_folder='static')

columns = [ 'column_1', 'column_2', 'column_3', 'column_4']
@datable.route('/')
def index():
    return render_template('datatables.html', columns=columns)
    return 'Hello World!'

@datable.route('/_server_data')
def get_server_data():
    
    collection = [dict(zip(columns, [1,2,3,4])), dict(zip(columns, [5,5,5,5]))]
    
    results = BaseDataTables(request, columns, collection).output_result()
    
    # return the results as a string for the datatable
    return jsonify(results)
