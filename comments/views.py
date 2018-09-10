from django.http import StreamingHttpResponse
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from comments.models import Comment
from comments.serializers import CommentSerializer
from comments.utils import comments_tree_stream


class CommentsViewSet(GenericViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    class Meta:
        model = Comment

    @action(detail=True)
    def children_tree(self, *args, **kwargs):
        """Returns children comments tree"""
        qs = Comment.objects.filter(pk=self.get_object().pk).with_children()
        return StreamingHttpResponse(comments_tree_stream(qs), content_type='application/json')





