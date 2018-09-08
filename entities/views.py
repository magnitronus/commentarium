from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from comments.views import CommentedEntityViewSetMixin, EntityTypes
from entities.models import Post
from entities.serializers import PostSerializer


class PostsViewSet(CommentedEntityViewSetMixin, ListModelMixin, GenericViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    entity_type = EntityTypes.blogpost
