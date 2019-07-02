from django.db import models

from conduit.apps.core.models import TimestampedModel
from .search import ArticleIndex


class Article(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)

    description = models.TextField()
    body = models.TextField()

    author = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE, related_name='articles'
    )

    tags = models.ManyToManyField(
        'articles.Tag', related_name='articles'
    )

    img = models.URLField(blank=True)

    def __str__(self):
        return self.title

    def indexing(self):
        obj = ArticleIndex(
            meta={'id': self.id}, author=self.author.user.username, created_at=self.created_at,
            updated_at=self.updated_at, title=self.title, body=self.body, description=self.description,
            slug=self.slug, tags=str(self.tags)
        )
        obj.save()
        return obj.to_dict(include_meta=True)


class Comment(TimestampedModel):
    body = models.TextField()

    article = models.ForeignKey(
        'articles.Article', related_name='comments', on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        'profiles.Profile', related_name='comments', on_delete=models.CASCADE
    )


class Tag(TimestampedModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag
