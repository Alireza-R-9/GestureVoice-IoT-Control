import socket

# TCP server configuration
HOST = "127.0.0.1"   # localhost (for test)
PORT = 5055          # must match the client port

def start_server():
    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"✅ Test server is running on {HOST}:{PORT} ...")
    print("Waiting for client connection...")

    while True:
        conn, addr = server_socket.accept()
        print(f"📡 Connected by {addr}")

        while True:
            try:
                # Receive data (max 1024 bytes)
                data = conn.recv(1024)
                if not data:
                    break  # connection closed

                message = data.decode("utf-8")
                print(f"➡️ Received: {message}")

                # Example response back to client
                response = f"ACK: {message}"
                conn.sendall(response.encode("utf-8"))

            except ConnectionResetError:
                print("⚠️ Connection lost!")
                break

        conn.close()
        print("❌ Client disconnected. Waiting for new connection...")

if __name__ == "__main__":
    start_server()
