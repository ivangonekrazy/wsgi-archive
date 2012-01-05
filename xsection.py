import sys, os.path
import json
import traceback
from zipfile import ZipFile
from wsgiref.validate import validator
from wsgiref.simple_server import make_server
from wsgiref.util import request_uri

def application(environ, start_response):

    def response(content, status="200 OK"):
        """ Response builder; attempts to JSON-encode
            non-strings
        """

        if isinstance(content, str):
            resp_headers = \
                [('Content-type', 'text/plain'), ('Content-length', str(len(content))) ]
            start_response(status, resp_headers)
            return [content]
        else:
            json_content = json.dumps(content)
            resp_headers = \
                [('Content-type', 'application/json'), ('Content-length', str(len(json_content))) ] 
            start_response(status, resp_headers)
            return [json_content]

    path = environ.get('PATH_INFO').lstrip('/')

    if path == '':
        return response(str(e), '404 Not Found')

    try:

        split_path = path.split('/', 1)

        # just the JSON index of the archive
        if len(split_path) == 1:
            zipfile = ZipFile(path, 'r')
            return response({
                "comment": zipfile.comment,
                "files": sorted(zipfile.namelist() ),
                "file_count": len(zipfile.namelist())
            })

        # extract a file from the archive
        else:
            zippath, file = split_path
            zipfile = ZipFile(zippath, 'r')
            try:
                return response( zipfile.read(file) )
            except KeyError, e:
                return response(str(e), '404 Not Found')

    except IOError, e:
        return response(str(e), '404 Not Found: %s' % path)
    except Exception, e:
        traceback.print_exc()
        return response(str(e), '500 Server Error')

# run standalone if we're invoked from the command-line
if __name__ == '__main__':
    PORT = 8000
    httpd = make_server('', PORT, validator(application))
    print 'Server listening at %s' % ( PORT )
    print 'ctrl-c to kill me ...'
    httpd.serve_forever()
