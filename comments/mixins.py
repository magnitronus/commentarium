from enum import Enum

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from comments.models import Comment
from comments.serializers import CommentSerializer, CommentTreeSerializer, CommentHistoryRequestSerializer
from comments.utils import comments_tree_stream
from entities.models import Post


class EntityTypes(Enum):
    userpage = ContentType.objects.get_for_model(get_user_model())
    blogpost = ContentType.objects.get_for_model(Post)


class ExportCommentsHistoryMixin:

    def get_comments_history_queryset(self):
        raise NotImplementedError('This method should be implemented for exporting comments')

    @action(detail=True)
    def comments_history(self, request, *args, **kwargs):
        request_serializer = CommentHistoryRequestSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)
        writer = request_serializer.validated_data.get('output')
        qs = self.get_comments_history_queryset()
        start_date = request_serializer.validated_data.get('start')
        end_date = request_serializer.validated_data.get('end')
        if start_date:
            qs = qs.filter(created__gte=start_date)
        if end_date:
            qs = qs.filter(created__lte=end_date)
        stream = writer(qs)
        response = StreamingHttpResponse(stream, content_type=writer.content_type)
        response['Content-Disposition'] = f'attachment; filename="comments.{writer.file_extension}"'
        return response


class CommentedEntityViewSetMixin(ExportCommentsHistoryMixin):

    entity_type: EntityTypes = None

    def get_comments_history_queryset(self):
        return Comment.objects.filter(
            entity_type=self.entity_type.value,
            entity_id=self.get_object().pk
        ).order_by('-created')

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
        serializer.save(entity_type=self.entity_type.value, entity_id=pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True)
    def comments(self, *args, **kwargs):
        """Get first level comments for entity"""
        page = self.paginate_queryset(self.entity_comments_queryset)
        serializer = CommentSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True)
    def comments_tree(self, *args, **kwargs):
        """Get comments tree"""
        qs = self.entity_comments_queryset.with_children()
        return StreamingHttpResponse(comments_tree_stream(qs), content_type='application/json')
