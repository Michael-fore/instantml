

from Flask import flask
from bluesprints.ai import bp as ai

app = Flask(__name__)

#app.register_blueprint(ai)

@app.route('/', methods=['GET'])
def index():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)