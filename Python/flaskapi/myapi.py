from flask import Flask, jsonify, request, Response
from classes.mycar import Car
from functools import wraps

# Create a Flask application instance
app = Flask(__name__)

@app.route('/api/', methods=['GET'])
def hello():
    # Return a JSON response
    return jsonify({'message': 'Hello, From Flask API!'})

@app.route('/api/car', methods=['POST'])
def handle_car_request():
    data = request.get_json()
    try:
        make=data.get('make'),
        model=data.get('model'),
        year=data.get('year')
        if not all([make, model, year]):
            raise ValueError("Missing required fields: make, model, year")
        car = Car(
            make=make,
            model=model,
            year=year
        )
        return jsonify(car.to_dict()), 201
    except ValueError as e1:
        return jsonify({'error': str(e1)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Basic authentication example
VALID_USERNAME = 'admin'
VALID_PASSWORD = 'secret'

def check_auth(username, password):
    return username == VALID_USERNAME and password == VALID_PASSWORD

def authenticate():
    return Response("Could not validate your credentials", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/protected')
@requires_auth
def protected():
    return jsonify({'message': 'Your are authenticated!'})
#Stopg basic authentication implementation

if __name__ == '__main__':
    app.run(debug=True)