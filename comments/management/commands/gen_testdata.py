from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db.models.expressions import Random
from tqdm import tqdm

from comments.factories import CommentFactory
from comments.models import Comment

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

    def handle(self, *args, **options):
        count = options.get('count')
        depth = options.get('depth')
        if count / depth < 10:
            raise Exception('The count should be at least 10 times larger than the depth')
        self.stdout.write('Run  "%s"...' % __name__.split('.')[-1])
        roots_count = int(count // depth // 2)
        self.stdout.write('Create tree')
        with tqdm(total=roots_count*depth) as pbar:
            for root_idx in range(roots_count):
                parent = None
                for depth_idx in range(depth):
                    parent = CommentFactory.create(parent=parent)
                    pbar.update()
        remain_count = count - roots_count*depth
        random_comments = Comment.objects.annotate(random=Random()).order_by('random')[:remain_count]
        remain_comments = []
        self.stdout.write('Create remains')
        with tqdm(total=remain_count) as pbar:
            for random_comment in random_comments:
                remain_comments.append(CommentFactory.build(parent=random_comment))
                pbar.update()
            Comment.objects.bulk_create(remain_comments, batch_size=100)
