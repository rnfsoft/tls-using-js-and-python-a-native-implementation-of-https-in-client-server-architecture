from flask import Flask, jsonify, request
import json
from flask_cors import CORS, cross_origin
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from base64 import b64decode

app = Flask(__name__)
app.secret_key = "secret"

app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

def decrypt_content(encrypted_text):
    f = open("./keys/private.pem", "rb")
    key = str(f.read().decode('utf-8'))
    # print(key)
    pkey = RSA.importKey(key)
    cipher = PKCS1_OAEP.new(pkey, hashAlgo=SHA256)
    decrypted_message = cipher.decrypt(b64decode(encrypted_text))
    return decrypted_message.decode('utf-8')

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    try:
        etext = request.data.decode('utf-8')
        data = decrypt_content(etext)
        json_data = json.loads(data)

    except Exception as e:
        return jsonify({'status': str(e), 'message': 'Data error'})
    else:
        username = str(json_data['username']).strip()
        password = str(json_data['password']).strip()

        if username=="admin" and password=="password":
            return jsonify({'status': 'Success', 'message': 'Logged In'})
        else:
            return jsonify({'status': 'Fail', 'message': 'Invalid Credentials'})

if __name__ == "__main__":
    app.run()
