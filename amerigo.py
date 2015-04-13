#!/usr/bin/env python

import socket
import http.server
import threading
import struct
import geojson
import argparse
import logging as log

FILE = "./position.geojson"
UDP_ADDR = "0.0.0.0"
UDP_PORT = 49000


# Relate the dataset (integer key) to the data (list of values)
rosetta = {1: ["real_time", "total_time", "mission_time", "timer_time",
               "", "zulu_time", "local_time", "hobbs_time"],
           20: ["lat", "lon", "alt_amsl", "alt_agl",
                "on_rwy", "alt_ind", "lat_south", "lon_west"],
           17: ["pitch", "roll", "hdg_true", "hdg_mag",
                "", "", "", ""]
           }


class LoggingHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        log.info("{}: [{}] {}".format(self.address_string(),
                                      self.log_date_time_string(),
                                      *args))


def split_payload(l, size=36):
    """
    Split "l" into chunks of 36 pieces and yield each one
    """
    for i in range(0, len(l) // size):
        ret = l[size * i:size * (i + 1)]
        yield ret


def parse_stream(data):
    """
    Return a dictionary composed of the parsed binary 'data'.

    b'raw data' -> {x-plane data}
    data ::= binary literal
    """

    header = data[0:5]
    payload = data[5:]

    if header == b"DATA@":
        output = {}
        for piece in split_payload(payload):
            msg = struct.unpack_from("iffffffff", piece)
            data_set = msg[0]
            data = msg[1:]

            if data_set in rosetta:
                # Append the translated 'data_set' to the output dict
                output.update(dict(zip(rosetta[data_set], data)))
            else:
                log.warning("Couldn't parse: idx:{} data:{}".format(data_set, data))

        return output


def server(args):
    """
    Start the HTTP server
    """
    http_bind_addr = "127.0.0.1"
    http_bind_port = 8000
    handler = LoggingHTTPHandler

    httpd = http.server.HTTPServer((http_bind_addr, http_bind_port), handler)
    log.info("Serving HTTP on {}:{}".format(http_bind_addr, http_bind_port))
    httpd.serve_forever()


def interpret(args):
    """
    Bind to a socket, parse the input and write to file.
    """

    # Bind to an internet-facing UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((args.address, args.port))
    log.info("Binding to {}:{}".format(args.address, args.port))

    while True:
        # Receive with a buffer of 1024 bytes
        data, addr = udp_socket.recvfrom(1024)
        parsed = parse_stream(data)
        if parsed["lon"] and parsed["lat"]:
            point = geojson.Point((parsed["lon"], parsed["lat"]))
        feature = geojson.Feature(geometry=point)

        with open(args.output, mode="w") as f:
            f.write(str(feature))


# Main program stars here
if __name__ == "__main__":
    # Parse arguments
    args = argparse.ArgumentParser()
    args.add_argument("-p", "--port", type=int, default=UDP_PORT,
                      help="port to bind to (default: %(default)s)")
    args.add_argument("-a", "--address", default=UDP_ADDR,
                      help="address to bind to (default: %(default)s)")
    args.add_argument("-o", "--output", default=FILE,
                      help="file that shall be written (default: %(default)s)")
    args.add_argument("-d", "--debug", const=log.DEBUG, nargs="?",
                      dest="loglevel", default=log.WARNING,
                      help="turn on debugging")
    args.add_argument("-v", "--verbose", const=log.INFO, nargs="?",
                      dest="loglevel",
                      help="turn on verbose output")
    args = args.parse_args()

    log.basicConfig(level=args.loglevel)

    # Create interpreter thread and send it the arguments
    interpreter_thread = threading.Thread(target=interpret,
                                          name="interpreter",
                                          args=(args,))
    server_thread = threading.Thread(target=server,
                                     name="server",
                                     args=(args,))

    # Run the threads
    interpreter_thread.start()
    server_thread.start()
