import socket
import threading
from cryptography.fernet import Fernet


# Enter the key shared from the server below
key =
cipher = Fernet(key)


# Function to receive and decrypt messages from the server
def receive_messages(client_socket):
   while True:
       try:
           # Receives encrypted message
           encrypted_data = client_socket.recv(1024)
           if not encrypted_data:
               break
           # Decrypts it
           decrypted = cipher.decrypt(encrypted_data).decode()
           print(f"\r[Server] {decrypted}\n[You] ", end="")
       except:
           break


# Connects to the server and start the chat
def start_client():
   client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # Connects to server
   client.connect(('127.0.0.1', 9999))


   # Starts a thread to listen for incoming messages
   thread = threading.Thread(target=receive_messages, args=(client,))
   thread.daemon = True
   thread.start()


   # Loops to send messages to the server
   while True:
       msg = input("[You] ")
       encrypted_msg = cipher.encrypt(msg.encode())
       # Send to server
       client.send(encrypted_msg)


start_client()
