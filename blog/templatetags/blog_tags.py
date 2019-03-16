from django import template
from django.db.models import Sum

from blog.models import Blog

register = template.Library()


@register.simple_tag
def total_blogs():
    return Blog.objects.count()


@register.simple_tag
def total_views():
    return Blog.objects.annotate(total_reads=Sum('reads'))


@register.simple_tag
def total_comments():
    return Blog.objects.count()


@register.inclusion_tag('blog/hot_blog.html')
def hot_blogs(n=5):
    hots = Blog.objects.values('slug', 'title', 'id', 'reads').order_by('-reads')[:n]
    return {"hots": hots}


@register.inclusion_tag('blog/latest_blog.html')
def latest_blogs(n=5):
    latest_articles = Blog.objects.values('slug', 'title', 'id').order_by('-publish')[:n]
    return {"latest_blogs": latest_articles}

