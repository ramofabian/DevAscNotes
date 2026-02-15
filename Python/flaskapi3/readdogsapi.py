import jwt
from flask import Flask, jsonify, request, make_response
from classes.ingestdogs import ingestdogs
import datetime

# Create a Flask application instance
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
dog_init = ingestdogs()

# Authentication with Bearer token (JWT) example
def token_required(f):
    def decorated(*args, **kwargs):
        #Expecting the token to be in the format "{Athorization: Bearer <token>}"
        full_token = request.headers.get('Authorization')
        try:
            token = full_token.split(" ")[1] if full_token else None
        except Exception as e:
            print(e)
            return jsonify({'error': 'token is missing'}), 401
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
        ) + datetime.timedelta(seconds=180)}, app.secret_key, algorithm="HS256")
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

@app.route('/api/ingestdogs', methods=['POST'])
@token_required
def handle_ingestdogs_request():
    data = request.get_json()
    try:
        if len(data) == 0:
            raise ValueError("Empty data received")
        
        if not isinstance(data, dict):
            raise ValueError("Invalid data format: expected a JSON object") 
        
        if "doglist" in data.keys():
            for dog_data in data["doglist"]:
                name = dog_data.get('name')
                age = dog_data.get('age')
                breed = dog_data.get('breed')
                if not all([name, age, breed]):
                    raise ValueError("Missing required fields: name, age, breed")
                dog = dog_init.add_to_list(
                    name=name,
                    age=age,
                    breed=breed
                )
        else:
            name=data.get('name'),
            age=data.get('age'),
            breed=data.get('breed')
            if not all([name, age, breed]):
                raise ValueError("Missing required fields: name, age, breed")
            dog = dog_init.add_to_list(
                name=name,
                age=age,
                breed=breed
            )
        return jsonify(dog_init.inventory), 201
    except ValueError as e1:
        return jsonify({'error': str(e1)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)