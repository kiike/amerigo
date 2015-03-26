#!/usr/bin/env python

import amerigo
import unittest


class TestAmerigo(unittest.TestCase):
    def test_split_payload(self):
        """
        Check that we are getting 10 36-sized lists from a 360-item list
        from split_payload()
        """

        long_list = [n for n in range(0, 360)]
        split_list = [item for item in amerigo.split_payload(long_list)]
        self.assertEqual(len(split_list), 10)

    def test_parse_coords(self):
        """
        Check that we are getting a known, valid dictionary from its raw
        known source datastream
        """

        stream = b'DATA@\x14\x00\x00\x00d\xf5\x1dB\x1eY\xf3\xbe\x7fEqCE'
        stream += b'\xb5v>\x00\x00\x80?\x8d\xa7xC\x00\x00\x18B\x00\x00\x00\xc0'

        parsed = amerigo.parse(stream)

        expected = {'alt_agl': 0.2409258633852005,
                    'alt_amsl': 241.27146911621094,
                    'alt_ind': 248.6544952392578,
                    'lat': 39.48963928222656,
                    'lat_south': 38.0,
                    'lon': -0.4752892851829529,
                    'lon_west': -2.0,
                    'on_rwy': 1.0}

        self.assertEqual(parsed, expected)


if __name__ == "__main__":
    unittest.main()
