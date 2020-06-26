from flask import Blueprint, render_template, g, session, request, jsonify
from resource.RoutePlanning import RoutePlanning
import os
import json

RoutePlanning_bp = Blueprint('RoutePlanning', __name__, template_folder='templates',
                    static_folder='static')

@RoutePlanning_bp.route('/')
def index():
       return render_template('base.html')

@RoutePlanning_bp.route('/result')
def result():
    origins = [[121.60546, 25.28247],
           [121.84354, 25.10815],
           [121.52081, 25.19156],
           [121.55292, 25.27472],
           [121.43855, 25.17181],
           [121.42752, 25.10372],
           [121.54404, 25.29054],
           [121.50055, 25.06498],
           [121.44421, 24.97271],
           [121.53531, 25.29261]]
    min_path_length, min_path_list, gmp = RoutePlanning().get_shortest_map(localtion_list=origins)
    return render_template('rbase.html', myhtml=gmp, paths=min_path_list, length=min_path_length)