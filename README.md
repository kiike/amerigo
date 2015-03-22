Amerigo
=======

Amerigo is a [FLOSS] companion webapp for X-Plane. Its purpose is building a
moving map composed, viewable, and modifieable with, entirely, FLOSS software.
This is an alternative to [Xplage] because there might be people who won't want
to use Google Earth just to track our flights.


Installation
------------

1. Clone this repository: `git clone https://github.com/kiike/amerigo.git`.

2. Install the requirements with pip:

    ` pip install geojson`


Running the webapp
------------------

3. Run `amerigo.py`

4. Keeping `amerigo.py` running, execute a `python -m http.server 8080`

5. Open http://localhost:8080 with your web browser.


License
-------

This project is licensed under the OpenBSD/ISC license. Please check the
`LICENSE` file for details.


Development
-----------

This project is still in a very early stage of development. Contributions are
not only accepted, but also encouraged. Please submit pull requests or issues
with your feedback!


Planned features
----------------

This features will probably come in the very near future:

- Markers that show the heading of the flight

- Popup with information, such as altitude, speed, etc.

- Toggleable plane tracking, that is, always keep the plane centered


[Xplage]: http://www.chriskern.net/code/xplaneToGoogleEarth.html
[FLOSS]: https://en.wikipedia.org/wiki/Alternative_terms_for_free_software#FLOSS
