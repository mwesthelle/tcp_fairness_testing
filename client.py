import argparse
import socket

MSG_SIZE = 1024


def connect(ip: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        print(f"connected to {ip} on port {port}.")
        while True:
            s.send(b'X'*MSG_SIZE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Open a TCP connection and listen on a specified port")
    parser.add_argument('-p', '--port', required=True,
                        type=int, help="the port the server will listen to")
    parser.add_argument('--ip', required=True, help="the server's IP")
    args = parser.parse_args()
    connect(args.ip, args.port)
