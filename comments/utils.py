import json

from comments.serializers import CommentTreeSerializer


def comments_tree_stream(qs):
    yield '['
    prev = None
    for comment in qs.iterator():
        if prev is not None:
            yield f'{prev},'
        prev = json.dumps(CommentTreeSerializer(comment).data)
    yield prev
    yield ']'