from rest_framework.serializers import ModelSerializer

from entities.models import Post


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'author', 'text',)
