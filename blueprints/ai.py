from flask import Blueprint, render_template, request

bp = Blueprint('images', __name__,url_prefix='/ai')

@bp.route('/', methods=['GET'])
def index():
    return 'Working'


@bp.route('/images', methods=['GET','POST'])
def images():

    if request.method == 'GET':
        return 'GET' 
    
    elif request.method == 'POST':
        return 'GET'

@bp.route('/text', methods=['GET','POST'])
def text():

    if request.method == 'GET':
        return 'GET' 
    
    elif request.method == 'POST':
        return 'GET'    

@bp.route('/speech', methods=['GET','POST'])
def speech():

    if request.method == 'GET':
        return 'GET' 
    
    elif request.method == 'POST':
        return 'GET'    