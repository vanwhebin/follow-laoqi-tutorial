from django.db import models
from slugify import slugify
from django.utils import timezone
from django.contrib.auth.models import User


class Column(models.Model):
    column = models.CharField(max_length=100, default='', blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='column_category')

    class Meta:
        ordering = ('create_time', )

    def __str__(self):
        return self.column


class Blog(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=100, default="", unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField(max_length=5000, default='', blank=True)
    publish = models.DateTimeField(default=timezone.now)
    reads = models.PositiveIntegerField(default=1, blank=True)
    likes = models.PositiveIntegerField(default=1, blank=True)
    status = models.BooleanField(default=True, blank=True)
    column = models.ForeignKey(Column, related_name='category', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-publish', )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        # TODO 处理文章标签的问题
        # return JsonResponse({"args": args, 'kwarg': kwargs})
        # self.author = self.request.user
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    blog = models.ForeignKey(Blog, related_name='tag', on_delete=models.CASCADE)
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comment', on_delete=models.CASCADE)
    commentator = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    # avatar = models.ImageField(max_length=100, blank=True, null=True)
    body = models.TextField(max_length=800)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, blank=True)
    replied = models.BooleanField(default=False, blank=True)
    reply = models.ForeignKey('self', related_name='reply_comment', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('create_time', )

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator, self.blog.title)


