from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from slugify import slugify
from django.shortcuts import reverse


class ArticleColumn(models.Model):
    user = models.ForeignKey(User, related_name='article_column', on_delete=models.CASCADE)
    column = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticlePost(models.Model):
    author = models.ForeignKey(User, related_name='article', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, related_name='article_column', on_delete=models.CASCADE)
    body = models.TextField()
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("article:article_detail", args=[self.id, self.slug])
