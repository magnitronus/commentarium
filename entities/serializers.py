from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from entities.models import Post

User = get_user_model()


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'author', 'text',)


class UserPageSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email')


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')
