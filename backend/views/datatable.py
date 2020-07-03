from flask import Blueprint, render_template, g, session, request, jsonify
from backend import cache

datable = Blueprint('datable', __name__, template_folder='templates',
                    static_folder='static')


@datable.route('/')
@cache.cached(timeout=604800)
def index():
    columns = ['景點名稱', '簡介', '地址', '電話']
    return render_template('datatables.html', columns=columns)
