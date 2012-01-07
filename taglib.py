from functools import partial

class TagLib(object):
    """
    Utility class for making HTML

    TODO: handle singleton tags
    TODO: add unit tests
    """
    
    def __getattr__(self, name):
        return partial( self.make_tag, name)

    def make_tag(self, *args):

        tag = args[0]
        attrs = ""

        # looks like we have attribs in a dict
        if isinstance(args[1], dict):
            attrs = " " + " ".join( 
                ["%s=\"%s\"" % (k,v) for k,v in args[1].items() ] )
            content = "".join(isinstance(args[2],list) and args[2] or args[2:] )
        else:
            content = "".join(isinstance(args[1],list) and args[1] or args[1:] )

        return "<%s%s>%s</%s>" % \
            (tag, attrs, content, tag)

if __name__ == "__main__":
    t = TagLib()

    print t.div(t.p("hello"))
    print t.div({"id":"hello"}, "hello with attrs")
    print t.div( t.p("hello"), t.p("world"))
    print t.div({"class":"greeting"}, t.p({"class":"xxx"},"hello"), t.p("world"))
    print t.div([t.p("hello"), t.p("list")])
