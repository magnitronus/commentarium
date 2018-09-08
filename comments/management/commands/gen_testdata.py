import random

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db.models.expressions import Random
from tqdm import tqdm

from comments.factories import CommentFactory
from comments.models import Comment
from entities.factories import UserFactory, PostFactory
from entities.models import Post

User = get_user_model()

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--depth',
            type=int,
            dest='depth',
            default=100,
            help='Needed nesting depth',
        )

        parser.add_argument(
            '--count',
            type=int,
            dest='count',
            default=10**4,
            help='Needed nodes count',
        )

        parser.add_argument(
            '--cleanup',
            action='store_true',
            help='Cleanup database before generate data'
        )

    def handle(self, *args, **options):
        count = options.get('count')
        depth = options.get('depth')
        if count / depth < 10:
            raise Exception('The count should be at least 10 times larger than the depth')
        self.stdout.write('Run  "%s"...' % __name__.split('.')[-1])
        if options.get('cleanup'):
            self.stdout.write('Cleanup database')
            User.objects.all().delete()
            Post.objects.all().delete()
            Comment.objects.all().delete()
        users = [UserFactory() for _ in range(10)]
        entities = users + [PostFactory() for _ in range(10)]
        roots_count = int(count // depth // 2)
        self.stdout.write('Create tree')
        with tqdm(total=roots_count*depth) as pbar:
            for root_idx in range(roots_count):
                parent = None
                for depth_idx in range(depth):
                    cf_kwargs = dict(parent=parent, user=random.choice(users))
                    if parent is None:
                        cf_kwargs['entity'] = random.choice(entities)
                    parent = CommentFactory.create(**cf_kwargs)
                    pbar.update()
        remain_count = count - roots_count*depth
        remain_comments = []
        self.stdout.write('Create remains')
        with tqdm(total=remain_count) as pbar:
            for random_comment in range(remain_count):
                remain_comments.append(
                    CommentFactory.build(
                        parent=Comment.objects.annotate(
                            random=Random()).order_by('random').first(),
                        user=random.choice(users)))
                pbar.update()
            Comment.objects.bulk_create(remain_comments, batch_size=100)
