from flask import Flask, jsonify, request
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.secret_key = "secret"

app.config['CORS_HEADERS'] = "Content-Type"
cors = CORS(app)

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    try:
        json_data = json.loads(request.data.decode("utf-8"))
    except ValueError:
        return jsonify({'status': 'Fail', 'message': 'Data error'})
    else:
        username = str(json_data['username']).strip()
        password = str(json_data['password']).strip()

        if username=="admin" and password=="password":
            return jsonify({'status': 'Success', 'message': 'Logged In'})
        else:
            return jsonify({'status': 'Fail', 'message': 'Invalid Credentials'})

if __name__ == "__main__":
    app.run()