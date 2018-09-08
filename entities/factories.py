from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, SubFactory
from factory.fuzzy import FuzzyText

from entities.models import Post

User = get_user_model()


class UserFactory(DjangoModelFactory):

    username = FuzzyText()

    class Meta:
        model = User


class PostFactory(DjangoModelFactory):

    author = SubFactory(UserFactory)

    class Meta:
        model = Post