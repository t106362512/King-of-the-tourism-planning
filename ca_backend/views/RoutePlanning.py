from flask import Blueprint, render_template, g, session, request, jsonify, request, redirect, url_for
from models.model import ScenicSpotInfo
from resource.RoutePlanning import RoutePlanning
import os
import json

RoutePlanning_bp = Blueprint('RoutePlanning', __name__, template_folder='templates',
                    static_folder='static')

@RoutePlanning_bp.route('/')
def index():
       return render_template('base.html')

@RoutePlanning_bp.route('/result', methods=['POST', 'GET'])
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

    print(request.form.getlist('selected[]'))

    # result_dict = json.loads(ScenicSpotInfo.objects(Id__in=args['IdList']).only(RETURN_FIELD).to_json())
    min_path_length, min_path_list, gmp = RoutePlanning().get_shortest_map(localtion_list=origins)
    if request.method == 'POST':
        return redirect(url_for('RoutePlanning.result', myhtml=gmp, paths=min_path_list, length=min_path_length))
    else:
        return render_template('rbase.html', myhtml=gmp, paths=min_path_list, length=min_path_length)