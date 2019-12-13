import argparse
import logging
import socket
import time

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
        logging.basicConfig(filename='bandwidth.log', filemode='a',
                            format='%(asctime)s - %(message)sMBps', level=logging.INFO)
        sock.bind(('', port))
        sock.listen(0)
        print(f"Listening on port {port}...")
        conn, addr = sock.accept()
        print(f"Accepted connection to {addr}")
        start_time = time.time()
        received_data = 0
        with conn:
            while True:
                data = conn.recv(BUFFER_SIZE)
                received_data += len(data)
                current_time = time.time()
                if a_second_has_elapsed(current_time, start_time):
                    # bandwidth per second is data received in that second
                    # multiplied by number of bits and divided by a Megabit
                    bandwidth_in_last_second = received_data * 8 / 2**20
                    logging.info(round(bandwidth_in_last_second, 2))
                    start_time = time.time()
                    received_data = 0
                if not data:
                    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Open a TCP connection and listen on a specified port')
    parser.add_argument('-p', '--port', required=True,
                        type=int, help='the port the server will listen to')
    args = parser.parse_args()
    listen(args.port)
