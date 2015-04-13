#!/usr/bin/env python
"""
This program is part of amerigo, a project to replace the utilities that
rely on Google Earth/Google Maps, and to play with building apps on top
of the X-Plane UDP interface.

Its functions are:
    * to receive the input of X-Plane via UDP
    * to translate the input into something we can work with
    * to build a GeoJSON file we can render with tools such as Leaflet
    * to start an HTTP server for easy serving of the files

Copyright (c) 2015 Enric Morales <me@enric.me>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import argparse
import geojson
import http.server
import logging as log
import socket
import struct
import sys
import threading

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
    """
    Turn the SimpleHTTPRequestHandler into a logging, simple
    request handler
    """

    def log_message(self, format, *args):
        log.info("{}: [{}] {}".format(self.address_string(),
                                      self.log_date_time_string(),
                                      *args))


def split_payload(l, size=36):
    """
    Yield every 36-byte chunk of `l`
    """

    for i in range(0, len(l) // size):
        ret = l[size * i:size * (i + 1)]
        yield ret


def parse_stream(input_bytes):
    """
    Return a dictionary composed of the parsed binary 'data'.

    b'raw data' -> {x-plane data}
    data ::= binary literal
    """

    header = input_bytes[0:5]
    payload = input_bytes[5:]

    if header == b"DATA@":
        output = {}
        for piece in split_payload(payload):
            msg = struct.unpack_from("iffffffff", piece)
            data_set = msg[0]
            data = msg[1:]
            # Uncomment to see what the program is receiving
            # log.info("idx:{} idx:{}".format(data_set, data))

            if data_set in rosetta:
                # Append the translated 'data_set' to the output dict
                output.update(dict(zip(rosetta[data_set], data)))
            else:
                msg = "Unimplemented data set idx:{} data:{}"
                log.warning(msg.format(data_set, data))

        # Uncomment to see the full dictionary (heaps of output!)
        # log.info(output)
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
