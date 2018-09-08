from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CommentQuerySet(models.QuerySet):

    def with_children(self):
        """
        Returns comments with all their children.
        Warning: It returns RawQuerySet to avoid additional annotate for ordering.
                All orm annotations before this method will be disabled.
        """
        base_query_str, base_query_params = (
            self.values_list('id', flat=True).query.sql_with_params())
        raw_sql = ("""WITH RECURSIVE 
            starting (id, parent_id, path) AS
            (
              SELECT t.id, t.parent_id, CAST(t.id AS text) AS path
              FROM {0} AS t
              WHERE t.id = ANY({1})
            ),
            descendants (id, parent_id, path) AS
            (
              SELECT s.id, s.parent_id, CAST(s.id AS text) AS path
              FROM starting AS s 
              UNION ALL
              SELECT t.id, t.parent_id, concat(d.path, '|', CAST(t.id AS text)) as path
              FROM {0} AS t JOIN descendants AS d ON t.parent_id = d.id
            ) SELECT t.*, d.path 
            FROM {0} AS t 
            JOIN descendants AS d 
            ON t.id = d.id ORDER BY path"""
                .format(self.model._meta.db_table, base_query_str))
        return self.model.objects.raw(raw_sql, base_query_params)


class CommentManager(models.Manager):

    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    text = models.CharField(max_length=500)
    entity_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    entity_id = models.PositiveIntegerField(blank=True, null=True)
    entity = GenericForeignKey('entity_type', 'entity_id')

    objects = CommentManager()
