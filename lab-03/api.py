from flask import Flask, request, jsonify
from cipher.rsa.rsa_cipher import RSACipher
from cipher.ecc import ECCCipher


print("API RSA LOADED")

app = Flask(__name__)

# RSA CIPHER ALGORITHM
rsa_cipher = RSACipher()

@app.route('/api/rsa/generate_keys', methods=['GET'])
def rsa_generate_keys():
    rsa_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})

@app.route("/api/rsa/encrypt", methods=["POST"])
def rsa_encrypt():
    data = request.json or {}
    message = data.get('message', '')
    key_type = data.get('key_type', 'public')
    private_key, public_key = rsa_cipher.load_keys()

    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type'}), 400

    encrypted_message = rsa_cipher.encrypt(message, key)
    encrypted_hex = encrypted_message.hex()

    return jsonify({'encrypted_message': encrypted_hex})


@app.route("/api/rsa/decrypt", methods=["POST"])
def rsa_decrypt():
    data = request.json or {}
    ciphertext_hex = data.get('ciphertext', '')
    key_type = data.get('key_type', 'private')
    private_key, public_key = rsa_cipher.load_keys()

    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type'}), 400

    try:
        ciphertext = bytes.fromhex(ciphertext_hex)
    except Exception:
        return jsonify({'error': 'Invalid ciphertext hex'}), 400

    decrypted_message = rsa_cipher.decrypt(ciphertext, key)

    return jsonify({'decrypted_message': decrypted_message})


@app.route('/api/rsa/sign', methods=['POST'])
def rsa_sign_message():
    data = request.json or {}
    message = data.get('message', '')
    private_key, _ = rsa_cipher.load_keys()

    signature = rsa_cipher.sign(message, private_key)
    signature_hex = signature.hex()

    return jsonify({'signature': signature_hex})


@app.route('/api/rsa/verify', methods=['POST'])
def rsa_verify_signature():
    data = request.json or {}
    message = data.get('message', '')
    signature_hex = data.get('signature', '')

    # load_keys returns (private_key, public_key)
    _, public_key = rsa_cipher.load_keys()

    try:
        signature = bytes.fromhex(signature_hex)
    except Exception:
        return jsonify({'error': 'Invalid signature hex'}), 400

    is_verified = rsa_cipher.verify(message, signature, public_key)

    return jsonify({'is_verified': is_verified})


# CAESAR CIPHER ENDPOINTS
def caesar_encrypt(text, key):
    try:
        k = int(str(key).strip()) % 26
    except Exception:
        k = 0
    out = []
    for ch in text:
        if 'a' <= ch <= 'z':
            out.append(chr((ord(ch) - 97 + k) % 26 + 97))
        elif 'A' <= ch <= 'Z':
            out.append(chr((ord(ch) - 65 + k) % 26 + 65))
        else:
            out.append(ch)
    return ''.join(out)

def caesar_decrypt(text, key):
    try:
        k = int(str(key).strip()) % 26
    except Exception:
        k = 0
    return caesar_encrypt(text, -k)


@app.route("/api/caesar/encrypt", methods=["POST"])
def api_caesar_encrypt():
    data = request.json or {}
    plain_text = data.get("plain_text", "")
    key = data.get("key", "0")
    encrypted = caesar_encrypt(plain_text, key)
    return jsonify({"encrypted_message": encrypted})


@app.route("/api/caesar/decrypt", methods=["POST"])
def api_caesar_decrypt():
    data = request.json or {}
    cipher_text = data.get("cipher_text", "")
    key = data.get("key", "0")
    decrypted = caesar_decrypt(cipher_text, key)
    return jsonify({"decrypted_message": decrypted})


# ECC CIPHER ALGORITHM
ecc_cipher = ECCCipher()

@app.route('/api/ecc/generate_keys', methods=['GET'])
def ecc_generate_keys():
    ecc_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})


@app.route('/api/ecc/sign', methods=['POST'])
def ecc_sign_message():
    data = request.json
    message = data['message']
    private_key, _ = ecc_cipher.load_keys()
    signature = ecc_cipher.sign(message, private_key)
    signature_hex = signature.hex()
    return jsonify({'signature': signature_hex})


@app.route('/api/ecc/verify', methods=['POST'])
def ecc_verify_signature():
    data = request.json
    message = data['message']
    signature_hex = data['signature']
    public_key, _ = ecc_cipher.load_keys()
    signature = bytes.fromhex(signature_hex)
    is_verified = ecc_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})

# main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)