Amerigo
=======

Amerigo is a [FLOSS] companion webapp for X-Plane. Its purpose is building a
moving map composed, viewable, and modifieable with, entirely, FLOSS software.
This is an alternative to [Xplage] because there might be people who won't want
to use Google Earth just to track our flights.

Requirements
------------

* X-Plane 10 properly configured to send the 20th dataset in "Data Input & Output" via UDP

* An open UDP port to receive the X-Plane data from

* Python 3 and [GeoJSON]

Installation
------------

1. Clone this repository: `git clone https://github.com/kiike/amerigo.git`.

2. Install the requirements with pip: `pip install -r requirements.txt`


Running the webapp
------------------

1. Run `amerigo.py`

2. Open http://localhost:8000 with your web browser.


License
-------

This project is licensed under the OpenBSD/ISC license (check the `LICENSE` file
for details) except for the
files/directories under the following list.

* `es_airspace.geojson` adapted from the [VueloAVela] KML file, subject to
  Vuelo a Vela's own copyright terms.

* `plane.png` by [FlatIcon], licensed under the [CC BY 3.0]


Development
-----------

This project is still in a very early stage of development. Contributions are
not only accepted, but also encouraged. Please submit pull requests or issues
with your feedback!


[Xplage]: http://www.chriskern.net/code/xplaneToGoogleEarth.html
[FLOSS]: https://en.wikipedia.org/wiki/Alternative_terms_for_free_software#FLOSS
[VueloAVela]: http://www.vueloavela.org/index.php/navegacion/cartografia
[FlatIcon]: http://www.flaticon.com
[CC BY 3.0]: http://creativecommons.org/licenses/by/3.0/
[GeoJSON]: https://github.com/frewsxcv/python-geojson
