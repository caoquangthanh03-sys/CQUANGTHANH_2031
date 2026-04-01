import socket
import threading
import sys
from tkinter import *

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad

# ====== SOCKET + KEY ======
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

client_key = RSA.generate(2048)

server_public_key = RSA.import_key(client_socket.recv(2048))
client_socket.send(client_key.publickey().export_key(format='PEM'))

encrypted_aes_key = client_socket.recv(2048)
cipher_rsa = PKCS1_OAEP.new(client_key)
aes_key = cipher_rsa.decrypt(encrypted_aes_key)

# ====== CRYPTO ======
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

# ====== UI ======
window = Tk()
window.title("Secure Chat (RSA + AES)")
window.geometry("500x500")

chat_area = Text(window, height=20, width=60)
chat_area.pack(pady=10)

msg_entry = Entry(window, width=40)
msg_entry.pack(side=LEFT, padx=10)

def send_message():
    message = msg_entry.get()
    if message == "":
        return

    encrypted = encrypt_message(aes_key, message)
    client_socket.send(encrypted)

    chat_area.insert(END, "You: " + message + "\n")
    msg_entry.delete(0, END)

    if message == "exit":
        client_socket.close()
        window.quit()

send_btn = Button(window, text="Send", command=send_message)
send_btn.pack(side=LEFT)

# ====== RECEIVE ======
def receive_messages():
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
            decrypted = decrypt_message(aes_key, encrypted_message)

            chat_area.insert(END, "Server: " + decrypted + "\n")
            chat_area.see(END)
        except:
            break

threading.Thread(target=receive_messages, daemon=True).start()

window.mainloop()