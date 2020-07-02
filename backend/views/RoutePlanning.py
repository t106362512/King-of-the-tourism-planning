from flask import Blueprint, render_template, g, session, request, jsonify, request, redirect, url_for
from backend.models.model import ScenicSpotInfo
from backend.resource.RoutePlanning import RoutePlanning
# from api.RoutePlanning import RoutePlanning as APIRP
from backend.api.ScenicSpot import ScenicSpot as APISS

RoutePlanning_bp = Blueprint('RoutePlanning', __name__, template_folder='templates',
                             static_folder='static')


@RoutePlanning_bp.route('/')
def index():
    return render_template('base.html')

@RoutePlanning_bp.app_errorhandler(404)
def handle_404(err):
    return render_template('hanlder/404.html'), 404

@RoutePlanning_bp.app_errorhandler(500)
def handle_500(err):
    return render_template('hanlder/500.html'), 500


@RoutePlanning_bp.route('/result', methods=['POST', 'get'])
def result():
    select_id = request.form.getlist('selected[]')
    print('select_id = {}'.format(select_id))
#     select_id = ['C1_A25000000E_000003', 'C1_387000000A_000161', 'C1_397000000A_000221', 'C1_397000000A_000634', 'C1_376550000A_000086', 'C1_376540000A_001295', 'C1_315081100H_000368', 'C1_376420000A_000430', 'C1_376420000A_000019', 'C1_376440000A_000853']

    ssinfo_by_id = APISS().post(args_dict={'IdList': select_id})['data']
    loc_list = [apiss_info['Location'] for apiss_info in ssinfo_by_id]
    name_list = [apiss_info['Name'] for apiss_info in ssinfo_by_id]
    id_list = [apiss_info['Id'] for apiss_info in ssinfo_by_id]
    min_path_length, min_path_list, min_mapping_path_list, gmp = RoutePlanning().get_shortest_map(localtion_list=loc_list, mapping_list=id_list)
    columns = ["Index", "景點名稱", "簡介", "地址", "電話", "空氣監測", "雨量監測"]

    return render_template('recommend.html', columns=columns, myhtml=gmp, mapping_paths=min_mapping_path_list, id_list=id_list, loc_list=min_path_list, length=min_path_length)