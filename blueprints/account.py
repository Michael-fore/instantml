from flask import Blueprint, render_template, request

bp = Blueprint('account', __name__,url_prefix='/account')

@bp.route('/signup', methods=['POST'])
def signup():
    return 'Working'

@bp.route('/login', methods=['POST'])
def login():
    return 'Working'

@bp.route('/logout', methods=['GET'])
def logout():
    return 'Working'

@bp.route('/api-key')
def api():
    return 'blah'