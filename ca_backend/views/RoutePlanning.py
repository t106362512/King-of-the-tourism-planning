from flask import Blueprint, render_template, g, session, request, jsonify, request, redirect, url_for
from models.model import ScenicSpotInfo
from resource.RoutePlanning import RoutePlanning
# from api.RoutePlanning import RoutePlanning as APIRP
from api.ScenicSpot import ScenicSpot as APISS

import os
import json

RoutePlanning_bp = Blueprint('RoutePlanning', __name__, template_folder='templates',
                    static_folder='static')

@RoutePlanning_bp.route('/')
def index():
       return render_template('base.html')

@RoutePlanning_bp.route('/result', methods=['POST'])
def result():
    select_id = request.form.getlist('selected[]')
    # a = APIRP().post(Id=select_id)
    ssinfo_by_id = APISS().post(args_dict={'IdList': select_id})['data']
    loc_list = [ apiss_info['Location'] for apiss_info in ssinfo_by_id]
    name_list = [ apiss_info['Name'] for apiss_info in ssinfo_by_id]
    id_list = [ apiss_info['Id'] for apiss_info in ssinfo_by_id]
    min_path_length, min_path_list, min_mapping_path_list, gmp = RoutePlanning().get_shortest_map(localtion_list=loc_list, mapping_list=name_list)
    columns = ["1", "2", "3", "4", "5"]
    return render_template('RoutePlanning.html', columns=columns, myhtml=gmp, mapping_paths=min_mapping_path_list, id_list=id_list, loc_list=min_path_list, length=min_path_length)