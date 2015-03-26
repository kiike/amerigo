#!/usr/bin/env python

import socket
import struct
import geojson

FILE = "./position.geojson"
UDP_IP = "0.0.0.0"
UDP_PORT = 49000

rosetta = {20: ["lat", "lon", "alt_amsl", "alt_agl",
                "on_rwy", "alt_ind", "lat_south", "lon_west"]}


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
                print("[ERROR] Couldn't parse:", data)

        return output


def main():
    # Bind to an internet-facing UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((UDP_IP, UDP_PORT))

    while True:
        # Receive with a buffer of 1024 bytes
        data, addr = udp_socket.recvfrom(1024)
        parsed = parse(data)
        point = geojson.Point(parsed["lon"], parsed["lat"],
                              parsed["alt_amsl"])
        feature = geojson.Feature(geometry=point)

        with open(FILE, mode="w") as f:
            f.write(str(feature))


# Main program stars here
if __name__ == "__main__":
    main()
