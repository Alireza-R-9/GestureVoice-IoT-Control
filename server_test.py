import socket
import threading
import datetime

# Server configuration
HOST = "127.0.0.1"  # Localhost
PORT = 5055  # TCP port for incoming connections


def handle_client(conn, addr):
    """
    Handle communication with a single client.
    This function runs in a separate thread for each client.

    Args:
        conn (socket.socket): The client socket object.
        addr (tuple): Client's address (IP, port).
    """
    print(f"📡 Connected by {addr}")
    with conn:
        while True:
            try:
                # Receive up to 1024 bytes from client
                data = conn.recv(1024)
                if not data:
                    break  # Client disconnected
                message = data.decode("utf-8")
                # Log received message with timestamp and client address
                print(f"{datetime.datetime.now()} ➡️ {addr} : {message}")
                # Send acknowledgment back to client
                response = f"ACK: {message}"
                conn.sendall(response.encode("utf-8"))
            except ConnectionResetError:
                print(f"⚠️ Connection lost with {addr}")
                break
    print(f"❌ Client {addr} disconnected")


def start_server():
    """
    Start a multi-client TCP server.
    Listens for incoming client connections and spawns a new thread for each client.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"✅ Multi-client server running on {HOST}:{PORT}")

        try:
            while True:
                # Accept new client connection
                conn, addr = server_socket.accept()
                # Start a new thread to handle the client independently
                client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                client_thread.daemon = True  # Daemon threads exit automatically on program termination
                client_thread.start()
        except KeyboardInterrupt:
            print("\n⚠️ Server stopped by user.")


if __name__ == "__main__":
    start_server()
