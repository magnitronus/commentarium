import json
import random
import time

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from comments.factories import CommentFactory
from comments.models import Comment
from entities.factories import UserFactory

User = get_user_model()

class CommentsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        parent = None
        roots = []
        for _ in range(100):
            parent = CommentFactory(user=cls.user, entity=cls.user, parent=parent)
            roots.append(parent)
        for _ in range(10**4):
            CommentFactory(user=cls.user, entity=cls.user, parent=random.choice(roots))

    def test_create_comment(self):
        url = reverse('userpages-comment', args=(self.user.id,))
        data = {'text': 'Test comment', 'user': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tree(self):
        root_comment = Comment.objects.get(parent__isnull=True)
        url = reverse('comments-children-tree', args=(root_comment.id,))
        response = self.client.get(url)
        response_text = ''.join([b.decode('utf-8') for b in response.streaming_content])
        self.assertEqual(len(json.loads(response_text)), 10**4+100)

    def test_query_time(self):
        start = time.time()
        Comment.objects.filter(parent__isnull=True).with_children()
        end = time.time() - start
        self.assertLess(end, 1)

