import sys, os.path
import json
import traceback

from zipfile import ZipFile
from rarfile import RarFile
from wsgiref.validate import validator
from wsgiref.simple_server import make_server
from wsgiref.util import request_uri

from taglib import TagLib

def ArchiveFile(path, mode='r'):
    """ Abstract away the difference between zip and rars
        ZipFile and RarFile have similar API's
        makes this easy.
    """

    root, ext = os.path.splitext(path)

    if ext.lower() == ".zip":
        return ZipFile(path, mode)
    elif ext.lower() == ".rar":
        return RarFile(path, mode)

def application(environ, start_response):

    def response(content, status="200 OK", content_type="text/plain"):
        """ Response builder;
            attempts to JSON-encode non-strings
        """

        if isinstance(content, str):
            resp_headers = \
                [('Content-type', content_type), ('Content-length', str(len(content))) ]
            start_response(status, resp_headers)
            return [content]
        else:
            json_content = json.dumps(content)
            resp_headers = \
                [('Content-type', 'application/json'), ('Content-length', str(len(json_content))) ] 
            start_response(status, resp_headers)
            return [json_content]


    # remove the leading slash;
    # don't confuse it with the root on the filesystem
    archive_path = environ.get('PATH_INFO').lstrip('/')

    # skip paths in the blacklist
    if archive_path in ['', 'favicon.ico']:
        return response("", '404 Not Found')

    #print environ['PATH_INFO']
    #print environ['REQUEST_METHOD']
    #print environ['QUERY_STRING']
    #print {
    #    k:v for k,v in environ.items() if k.startswith("HTTP")
    #}

    query_string = environ.get('QUERY_STRING')

    try:

        # split the archive path off,
        # preserve the path within the archive
        split_path = archive_path.split('/', 1)

        # just the JSON index of the archive
        if len(split_path) == 1:

            archive = ArchiveFile(archive_path, 'r')
            names = archive.namelist()

            # build an HTML index
            if query_string == "index":

                _ = TagLib()
                html = _.html(
                    _.body(
                        _.h4( archive.comment or archive_path ),
                        _.ol([
                            _.li(
                                _.a({"href":"%s/%s" % (archive_path,n)}, n) )
                            for n in sorted(names)
                        ])
                    )
                )

                return response( str(html), content_type="text/html")

            # return an inventory in JSON
            else:
                return response({
                    "comment": archive.comment,
                    "files": sorted(names),
                    "file_count": len(names)
                })

        # extract a file from the archive
        else:
            archive_path, file = split_path
            archive = ArchiveFile(archive_path, 'r')
            try:
                return response( archive.read(file) )
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
