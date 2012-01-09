# WSGI-Archive
## RESTful Archives via WSGI

### Dependencies

* RarFile

These can be installed via PIP by running:
`pip install -r pip-requirements.txt`

RarFile itself depends on `unrar`, which can be installed via:

* Ubuntu: `apt-get install unrar`
* OSX:  `brew install unrar`

### Running the app

To run a standalone server:

`python wsgi-archive.py`

The server will listen on port 8000 by default.
Any __.zip__ or __.rar__ file in the current directory
will be exposed via the path of the URL.

e.g. __foo.zip__ on the current directory will be exposed
at __http://localhost:8000/foo.zip__

Files within the archive are exposed relative to the 
archive file.

e.g. __/bar/baz.jpg__ in __foo.zip__ are exposed at
at __http://localhost:8000/foo.zip/bar/baz.jpg__
