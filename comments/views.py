from enum import Enum

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from comments.models import Comment
from comments.serializers import CommentSerializer
from entities.models import Post


class EntityTypes(Enum):
    userpage = ContentType.objects.get_for_model(get_user_model())
    blogpost = ContentType.objects.get_for_model(Post)


class CommentsViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    class Meta:
        model = Comment

    @action(detail=True)
    def children(self, *args, **kwargs):
        """Return first level children comments"""
        serializer = self.serializer_class(
            self.get_object().children.all(), many=True)
        return Response(serializer.data)


class CommentedEntityViewSetMixin:

    entity_type: EntityTypes = None

    def _get_list_comments_response(self, qs):
        serializer = CommentSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @property
    def entity_comments_queryset(self):
        return Comment.objects.filter(
            entity_type=self.entity_type.value,
            entity_id=self.get_object().pk,
            parent__isnull=True)

    @action(methods=['post'], detail=True)
    def comment(self, request, *args, **kwargs):
        """Create comment for entity"""
        pk = self.get_object().pk
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        save_kwargs = ( # Add entity identifier if no parent comment
            dict(entity_type=self.entity_type, entity_id=pk)
            if not serializer.validated_data.get('parent') else dict())
        serializer.save(**save_kwargs)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True)
    def comments(self, *args, **kwargs):
        """Get first level comments for entity"""
        return self._get_list_comments_response(self.entity_comments_queryset)

    @action(detail=True)
    def comments_tree(self, *args, **kwargs):
        """Get comments tree"""
        qs = self.entity_comments_queryset.with_children()
        return self._get_list_comments_response(qs)
