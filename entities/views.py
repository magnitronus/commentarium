from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from comments.serializers import CommentSerializer
from comments.mixins import CommentedEntityViewSetMixin, EntityTypes, ExportCommentsHistoryMixin
from entities.models import Post
from entities.serializers import PostSerializer, UserPageSerializer, UserSerializer

User = get_user_model()


class PostsViewSet(CommentedEntityViewSetMixin, ListModelMixin, GenericViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    entity_type = EntityTypes.blogpost


class UserPageViewSet(CommentedEntityViewSetMixin, ListModelMixin, GenericViewSet):
    serializer_class = UserPageSerializer
    queryset = User.objects.all()
    entity_type = EntityTypes.userpage


class UserViewSet(ExportCommentsHistoryMixin, ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_comments_history_queryset(self):
        return self.get_object().comments.all().order_by('-created')

    @action(detail=True)
    def comments(self, *args, **kwargs):
        page = self.paginate_queryset(self.get_comments_history_queryset())
        serializer = CommentSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
