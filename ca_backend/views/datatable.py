from flask import Blueprint, render_template, g, session, request, jsonify
from models.model import BaseDataTables
import os
import json

datable = Blueprint('datable', __name__, template_folder='templates',
                    static_folder='static')

@datable.route('/')
def index():
    columns = [ 'column_1', 'column_2', 'column_3', 'column_4']
    return render_template('datatables.html', columns=columns)