import argparse
from functools import partial
import logging
import socket
import time

MSG_SIZE = 1024


def a_second_has_elapsed(current_time: float, start_time: float) -> bool:
    """
    Given two timestamps (unix epochs), a starting time and a current time,
    checks if the current time is at least a second later than the starting
    time
    """
    return current_time - start_time >= 1


def connect(ip: str, port: int):
    logging.basicConfig(filename='bandwidth.log',
                        filemode='a',
                        format='%(asctime)s - %(message)sMBps',
                        level=logging.INFO)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        print(f"connected to {ip} on port {port}.")
        start_time = time.time()
        total_sent_data = 0
        for data in iter(partial(sock.send, b'x' * MSG_SIZE), b''):
            # sock.send returns amount of successfully sent bytes
            total_sent_data += data
            current_time = time.time()
            if a_second_has_elapsed(current_time, start_time):
                # bandwidth per second is data received in that second
                # multiplied by number of bits and divided by a Megabit
                bandwidth_in_last_second = total_sent_data * 8 / 2**20
                logging.info(round(bandwidth_in_last_second, 2))
                start_time = time.time()
                total_sent_data = 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Open a TCP connection and listen on a specified port")
    parser.add_argument('-p', '--port', required=True,
                        type=int, help="the port the server will listen to")
    parser.add_argument('--ip', required=True, help="the server's IP")
    args = parser.parse_args()
    connect(args.ip, args.port)
