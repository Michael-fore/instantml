from flask import Flask
from blueprints.ai import bp as ai

app = Flask(__name__)

#app.register_blueprint(ai)

@app.route('/', methods=['GET'])
def index():
    return 'Hello World'



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0 ')