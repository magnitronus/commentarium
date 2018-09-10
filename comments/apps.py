from importlib import import_module

from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = 'comments'

    def ready(self):
        import_module('comments.writers')
