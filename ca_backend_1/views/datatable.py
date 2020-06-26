from flask import Blueprint, render_template, g, session, request, jsonify
from models.model import BaseDataTables
import os
import json

datable = Blueprint('datable', __name__, template_folder='templates',
                    static_folder='static')


@datable.route('/')
def index():
    columns = ['景點名稱', '簡介', '地址', '電話']
    return render_template('datatables.html', columns=columns)
