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

Any ZIP or RAR file in the current directory
will be exposed via the path of the URL.

* Any ZIP or RAR file on the current directory will be exposed
at __http://localhost:8000/__
* __foo.zip__ on the current directory will be exposed
at __http://localhost:8000/foo.zip__

A URL that points to the application root or to just an archive
file will get an HTML index by default. The index format can be 
set with the __format={html,json}__ query parameter.

* __http://localhost:8000/baz.zip?format=html__ returns the index of 
the contents of __baz.zip__ as an HTML page. This is the default.

* __http://localhost:8000/?format=json__ returns the index of 
ZIP and RAR files in JSON format.
* __http://localhost:8000/foo.zip?format=json__ returns the index of 
__foo.zip__ JSON format.
* __http://localhost:8000/quux.rar?format=json__ returns the index of 
the contents of __quux.rar__ JSON format.

Files within the archive are exposed relative to the 
archive file.

* __/boo.png__ in __quux.rar__ are exposed at
at __http://localhost:8000/quux.rar/boo.png__
* __/bar/baz.jpg__ in __foo.zip__ are exposed at
at __http://localhost:8000/foo.zip/bar/baz.jpg__

The index can be passed a filter to show only files
within the archive that have file names that start
with a given value. 

* __http://localhost:8000/foo.zip?filter=bar__
will generate an index of all files that start with
__bar__, which may include __bar.jpg__ and __bar/__
