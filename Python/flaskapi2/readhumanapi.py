import jwt
from flask import Flask, jsonify, request, make_response
from classes.ingesthuman import ingesthuman
import datetime
# from functools import wraps

# Create a Flask application instance
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Authentication with web tokens (JWT) example
def token_required(f):
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        # token = request.get_json().get('token')
        print(token)
        if not token:
            return jsonify({'error': 'token is missing'}), 403
        try:
            jwt.decode(token, app.secret_key, algorithms=["HS256"])
        except Exception as error:
            print(error)
            return jsonify({'error': 'token is invalid/expired'})
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated


@app.route("/login")
def login():
    auth = request.authorization
    if auth and auth.password == "password":
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(seconds=180)}, app.secret_key)
        # return f'<a href="http://localhost:5000/access?token={token}">Private link</a>'
        return jsonify({'token': token})
    return make_response('Could not Verify', 401, {'WWW-Authenticate': 'Basic realm ="Login Required"'})


@app.route("/access")
@token_required
def access():
    return jsonify({'message': 'valid jwt token'})
#Stopg basic authentication implementation

@app.route('/api/', methods=['GET'])
@token_required
def hello():
    # Return a JSON response
    return jsonify({'message': 'Hello, From Flask API!'})

@app.route('/api/ingesthuman', methods=['POST'])
@token_required
def handle_ingesthuman_request():
    data = request.get_json()
    try:
        name=data.get('name'),
        age=data.get('age'),
        if not all([name, age]):
            raise ValueError("Missing required fields: name, age")
        human = ingesthuman(
            name=name,
            age=age
        )
        return jsonify(human.to_dict()), 201
    except ValueError as e1:
        return jsonify({'error': str(e1)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)