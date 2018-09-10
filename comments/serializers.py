from rest_framework.fields import SerializerMethodField, DateField
from rest_framework.serializers import ModelSerializer, Serializer

from comments.fields import OutputField
from comments.models import Comment


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'parent', 'user', 'created', 'text')

    def get_path(self, obj):
        return getattr(obj, 'path', None)


class CommentTreeSerializer(CommentSerializer):
    path = SerializerMethodField()

    class Meta:
        model = Comment
        fields = CommentSerializer.Meta.fields + ('path',)

    def get_path(self, obj):
        return getattr(obj, 'path', None)


class CommentHistoryRequestSerializer(Serializer):
    start = DateField(required=False)
    end = DateField(required=False)
    output = OutputField(required=False)
