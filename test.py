import xplane
import geojson


def test_parse_payload():
    msg = b"DATA@\x11\x00\x00\x00KbA@i\x98&\xbcn|\xe2A\x1b\x8a\xf3A"
    msg += b"\x00\xc0y\xc4\x00\xc0y\xc4\x00\xc0y\xc4\x00\xc0y\xc4\x14"
    msg += b"\x00\x00\x00d\xf5\x1dB\x1eY\xf3\xbe\x81EqC\xf0\xb7v>\x00"
    msg += b"\x00\x80?\x8e\xa7xC\x00\x00\x18B\x00\x00\x00\xc0"

    parsed = xplane.parse(msg)
    point = geojson.Point((parsed["lon"], parsed["lat"]))
    with open(FILE, mode="w") as f:
        f.write(str(geojson.Feature(geometry=point)))
