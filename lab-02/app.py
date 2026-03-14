from flask import Flask, render_template, request, json
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)

# router routes for home page
@app.route('/')
def home():
    return render_template('index.html')

# router routes for caesar cipher
@app.route('/caesar')
def caesar():
    return render_template('caesar.html')

# router routes for vigenere cipher
@app.route('/vigenere')
def vigenere():
    return render_template('vigenere.html')

# router routes for railfence cipher
@app.route('/railfence')
def railfence():
    return render_template('railfence.html')

# router routes for playfair cipher
@app.route('/playfair')
def playfair():
    return render_template('playfair.html')

# router routes for transposition cipher
@app.route('/transposition')
def transposition():
    return render_template('transposition.html')


# ================= CAESAR =================

@app.route('/encrypt', methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])

    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)

    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"


@app.route('/decrypt', methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])

    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)

    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"


# ================= VIGENERE =================

@app.route('/vigenere_encrypt', methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']

    Vigenere = VigenereCipher()
    encrypted_text = Vigenere.vigenere_encrypt(text, key)

    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"


@app.route('/vigenere_decrypt', methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']

    Vigenere = VigenereCipher()
    decrypted_text = Vigenere.vigenere_decrypt(text, key)

    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"


# ================= RAIL FENCE =================

@app.route('/railfence_encrypt', methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])

    RailFence = RailFenceCipher()
    encrypted_text = RailFence.encrypt(text, key)

    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"


@app.route('/railfence_decrypt', methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])

    RailFence = RailFenceCipher()
    decrypted_text = RailFence.decrypt(text, key)

    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"


# ================= PLAYFAIR =================

@app.route('/playfair_encrypt', methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']

    Playfair = PlayfairCipher()
    matrix = Playfair.create_playfair_matrix(key)
    encrypted_text = Playfair.playfair_encrypt(text, matrix)

    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"


@app.route('/playfair_decrypt', methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']

    Playfair = PlayfairCipher()
    matrix = Playfair.create_playfair_matrix(key)
    decrypted_text = Playfair.playfair_decrypt(text, matrix)

    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"


# ================= TRANSPOSITION =================

@app.route('/transposition_encrypt', methods=['POST'])
def transposition_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])

    Transposition = TranspositionCipher()
    encrypted_text = Transposition.encrypt(text, key)

    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"


@app.route('/transposition_decrypt', methods=['POST'])
def transposition_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])

    Transposition = TranspositionCipher()
    decrypted_text = Transposition.decrypt(text, key)

    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"


# main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)