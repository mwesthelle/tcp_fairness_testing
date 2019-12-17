import argparse
from functools import partial
import socket

BUFFER_SIZE = 2**10


def a_second_has_elapsed(current_time: float, start_time: float) -> bool:
    """
    Given two timestamps (unix epochs), a starting time and a current time,
    checks if the current time is at least a second later than the starting
    time
    """
    return current_time - start_time >= 1


def listen(port: int):
    """
    Listens on the specified port for TCP connections on any available IPv4
    interface
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', port))
        sock.listen(0)
        print(f"Listening on port {port}...")
        conn, addr = sock.accept()
        print(f"Accepted connection to {addr[0]}")
        with conn:
            for data in iter(partial(conn.recv, BUFFER_SIZE), b''):
                pass
        print(f"Connection to {addr[0]} was closed.")
        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Open a TCP connection and listen on a specified port')
    parser.add_argument('-p', '--port', required=True,
                        type=int, help='the port the server will listen to')
    args = parser.parse_args()
    listen(args.port)
