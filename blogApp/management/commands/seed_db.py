from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils.text import slugify

from blogApp.models import Post, PostHashtag, PostComment


class Command(BaseCommand):
    help = 'Populate the database with random posts, hashtags and comments'

    def handle(self, *args, **kwargs):
        fake = Faker()

        self.stdout.write(self.style.WARNING("Seeding the database..."))

        # Create hashtags
        hashtags = []
        for _ in range(10):
            title = fake.word()
            slug = slugify(title)
            obj, _ = PostHashtag.objects.get_or_create(title=title, slug=slug)
            hashtags.append(obj)



        # Create posts
        posts = []
        for _ in range(30):
            title = fake.sentence(nb_words=5)
            post = Post.objects.create(
                title=title,
                content=fake.paragraph(nb_sentences=10),
                stars=random.randint(1, 5),
            )
            post.tags.set(random.sample(hashtags, random.randint(0, min(5, len(hashtags)))))
            posts.append(post)

        # Create comments
        for post in posts:
            for _ in range(random.randint(0, 5)):
                PostComment.objects.create(
                    post=post,
                    name=fake.name(),
                    comment=fake.paragraph(nb_sentences=2)
                )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
