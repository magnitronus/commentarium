from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from comments.models import Comment


class CommentFactory(DjangoModelFactory):
    text = FuzzyText()

    class Meta:
        model = Comment
