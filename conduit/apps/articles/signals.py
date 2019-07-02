from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from conduit.apps.core.utils import generate_random_string
from .nlp import TextRank4Keyword
from .models import Article, Tag
tr4w = TextRank4Keyword()

@receiver(pre_save, sender=Article)
def add_slug_to_article_if_not_exists(sender, instance, *args, **kwargs):
    MAXIMUM_SLUG_LENGTH = 255
    if instance and not instance.slug:
        slug = slugify(instance.title)
        unique = generate_random_string()

        if len(slug) > MAXIMUM_SLUG_LENGTH:
            slug = slug[:MAXIMUM_SLUG_LENGTH]

        while len(slug + '-' + unique) > MAXIMUM_SLUG_LENGTH:
            parts = slug.split('-')

            if len(parts) is 1:
                slug = slug[:MAXIMUM_SLUG_LENGTH - len(unique) - 1]
            else:
                slug = '-'.join(parts[:-1])

        instance.slug = slug + '-' + unique

@receiver(post_save, sender=Article)
def add_tags(sender, instance, *args, **kwargs):
    if instance:
        tr4w.analyze(instance.body, candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
        keywords,weight = tr4w.get_keywords(10)
        for tag in keywords:
            instance.tags.add(Tag.objects.get_or_create(tag=tag, slug=tag.lower())[0])


@receiver(post_save, sender=Article)
def index_post(sender, instance, **kwargs):
    instance.indexing()
