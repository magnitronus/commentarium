from lxml import etree

__all__ = ('get_writer',)

__WRITERS_REGISTRY = {}


def comments_writer(name: str):
    def wrapper(cls):
        cls.writer_name = name
        __WRITERS_REGISTRY[name] = cls()
        return cls
    return wrapper


def get_writer(name: str = None):
    if name is None:
        return XmlWriter()
    return __WRITERS_REGISTRY.get(name, XmlWriter())


@comments_writer('xml')
class XmlWriter:

    content_type = 'text/xml'
    file_extension = 'xml'

    def __call__(self, qs):
        from comments.serializers import CommentSerializer
        for comment in qs.iterator():
            serializer = CommentSerializer(comment)
            rec = etree.Element(
                'comment', **{key: str(val) for key, val in serializer.data.items()})
            yield etree.tostring(rec)
