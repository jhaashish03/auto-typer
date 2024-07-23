import socket
import pyautogui
import time
import random
import threading

# Function to type text with random pauses
def type_text_with_pauses(text, stop_flag, start_index):
    for index in range(start_index, len(text)):
        if stop_flag[0]:  # Check if stop command received
            return index  # Return the current position
        pyautogui.write(text[index])
        # # Introduce a small random delay between keystrokes
        # time.sleep(random.uniform(0.0025, 0.005))
        # # Add a longer random pause between words
        # if text[index] in [' ', '\n']:
        #     time.sleep(random.uniform(0.05, 0.5))
    return len(text)  # Return the end of the text when done

# Function to handle typing in a separate thread
def typing_worker(text, stop_flag, current_index, resume_event, resume_index, connection):
    while not stop_flag[0] and current_index < len(text):
        if resume_event.is_set():
            current_index = type_text_with_pauses(text, stop_flag, resume_index[0])
            resume_index[0] = current_index  # Update the resume index
    if current_index >= len(text):
        send_typing_complete(connection)

# Function to send typing complete message to client
def send_typing_complete(connection):
    try:
        connection.sendall(b'typing_complete')
    except Exception as e:
        print(f"Error sending typing complete message: {e}")

# Function to handle a single client connection
def handle_client(connection, client_address):
    print(f"Connection from {client_address}")
    stop_flag = [False]
    resume_event = threading.Event()
    typing_thread = None
    current_index = 0
    resume_index = [0]
    text_to_type = ""

    try:
        while True:
            # Receive data from the client
            data = connection.recv(4096)
            if not data:
                break
            text = data.decode().strip()
            print(f"Received: {text}")

            if text == "stop":
                stop_flag[0] = True
                resume_event.clear()
                print("Typing stopped")
            elif text == "resume":
                if typing_thread is None or not typing_thread.is_alive():
                    stop_flag[0] = False
                    resume_event.set()
                    typing_thread = threading.Thread(target=typing_worker, args=(text_to_type, stop_flag, current_index, resume_event, resume_index, connection))
                    typing_thread.start()
                    print("Typing resumed from index", resume_index[0])
            else:
                if typing_thread is None or not typing_thread.is_alive():
                    text_to_type = text
                    stop_flag[0] = False
                    current_index = 0
                    resume_index[0] = 0  # Reset the resume index
                    resume_event.set()
                    typing_thread = threading.Thread(target=typing_worker, args=(text_to_type, stop_flag, current_index, resume_event, resume_index, connection))
                    typing_thread.start()
                else:
                    print("Still typing the previous message. Please wait.")

    finally:
        # Clean up the connection
        connection.close()
        print(f"Connection from {client_address} closed.")

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 12345)  # Choose any available port number
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)

print(f"Server is running on {server_address[0]}:{server_address[1]}")

try:
    while True:
        # Wait for a connection
        print("Waiting for a connection...")
        connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
        client_thread.start()

except KeyboardInterrupt:
    print("Server is shutting down.")

finally:
    # Clean up the server socket
    server_socket.close()
