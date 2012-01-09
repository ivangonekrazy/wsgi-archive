# WSGI-Archive
## RESTful Archives via WSGI

### Dependencies

* RarFile

These can be installed via PIP by running:
`pip install -r pip-requirements.txt`

### Running the app

To run a standalone server:

`python wsgi-archive.py`

The server will listen on port 8000 by default.
Any _.zip_ or _.rar_ file in the current directory
will be exposed via the path of the URL.

e.g. _foo.zip_ on the current directory will be exposed
at _http://localhost:8000/foo.zip_

Files within the archive are exposed relative to the 
archive file.

e.g. _/bar/baz.jpg_ in _foo.zip_ are exposed at
at _http://localhost:8000/foo.zip/bar/baz.jpg_
