import socket  # For network communication
import threading  # To handle sending and receiving at the same time
from cryptography.fernet import Fernet  # For encryption


# Generates a secret encryption key
key = Fernet.generate_key()
cipher = Fernet(key)


# Shows the key so it can be copied into the client
print("Your encryption key:", key)




# Function to handle incoming messages from the client
def handle_client(client_socket):
   while True:
       try:
           # Receives encrypted message from client
           encrypted_data = client_socket.recv(1024)
           if not encrypted_data:
               break
           # Decrypts and shows the message
           decrypted = cipher.decrypt(encrypted_data).decode()
           print(f"\r[Client] {decrypted}\n[You] ", end="")
       except:
           break




# Sets up and starts the server
def start_server():
   # Creates socket
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # Listens on port 9999
   server.bind(('0.0.0.0', 9999))
   # Allows only one connection
   server.listen(1)
   print("Server started. Waiting for a connection...")


   # Accepts connection from a client
   client_socket, addr = server.accept()
   print(f"Connected to {addr}")


   # Starts a thread to listen for messages from the client
   thread = threading.Thread(target=handle_client, args=(client_socket,))
   thread.daemon = True
   thread.start()


   # Loops to send messages to the client
   while True:
       msg = input("[You] ")
       # Encrypts message
       encrypted_msg = cipher.encrypt(msg.encode())
       # Sends to client
       client_socket.send(encrypted_msg)


start_server()
