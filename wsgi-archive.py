import sys, os.path
import json
import traceback

from zipfile import ZipFile
from rarfile import RarFile
from urlparse import parse_qsl
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

def build_index(names, archive_path, title="", comment="", index_format="html"):
    """ build and index """
    if index_format == "html":

        _ = TagLib()
        html = _.html(
            _.body(
                _.h4( title or archive_path ),
                _.h5( comment ),
                _.ol(
                    [
                    _.li(
                        _.a({"href":"%s/%s" % (archive_path,n)}, n) )
                    for n in sorted(names)
                    ]
                )
            )
        )

        return str(html), "text/html"

    # return an inventory in JSON
    elif index_format == "json":
        return {
            "comment": comment,
            "files": sorted(names),
            "file_count": len(names)
        }, "application/json"

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

    # grab the index format query string
    query_string = environ.get('QUERY_STRING')
    index_format = dict(parse_qsl(query_string)).get('format', 'html')
    file_filter = dict(parse_qsl(query_string)).get('filter', None)

    try:

        # split the archive path off,
        # preserve the path within the archive
        split_path = archive_path.split('/', 1)

        if len(split_path) > 1:
            archive_path, file = split_path
        else:
            file = ""

        archive = ArchiveFile(archive_path, 'r')
        names = archive.namelist()

        # just the index of the archive
        if len(split_path) == 1:

            # filter down to just matching files, if a filte was given
            if file_filter:
                names = filter(
                        lambda x: x.startswith(file_filter),
                        names)
                if len(names) == 0:
                    return response("Filter doesn't match any files.",
                        '404 Not Found')

            # build an HTML index
            title = archive_path
            comment = archive.comment or ""
            content, type = build_index(
                names, archive_path,
                title=title, comment=comment, index_format=index_format)

            return response( content, content_type=type)

        # extract a file from the archive
        else:
            return response( archive.read(file) )

    except IOError, e:
        return response(str(e), '404 Not Found: %s' % path)
    except KeyError, e:
        return response(str(e), '404 Not Found in archive: %s' % file)
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
