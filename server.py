import argparse
import socket

BUFFER_SIZE = 2**10
# HOST = '127.0.0.1'

def listen(port: int):
    """
    Listens on the specified port for TCP connections on any available IPv4 interface
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port))
        s.listen(0)
        print(f"Listening on port {port}...")
        conn, addr = s.accept()
        print(f"Accepted connection to {addr}")
        with conn:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Open a TCP connection and listen on a specified port')
    parser.add_argument('-p', '--port', required=True, type=int, help='the port the server will listen to')
    args = parser.parse_args()
    listen(args.port)
