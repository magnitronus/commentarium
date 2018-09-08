import itertools
import random

from django.contrib.auth import get_user_model
from factory import Sequence
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from comments.models import Comment
from entities.factories import UserFactory, PostFactory

User = get_user_model()

users = [UserFactory() for _ in range(10)]

posts = [PostFactory() for _ in range(10)]

entities = posts + users

class CommentFactory(DjangoModelFactory):
    user = Sequence(lambda _: random.choice(users))
    entity = Sequence(lambda _: random.choice(entities))
    text = FuzzyText()

    class Meta:
        model = Comment