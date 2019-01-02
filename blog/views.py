from django.shortcuts import render, get_object_or_404, HttpResponse
from blog.models import BlogArticles


def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request, 'blog/titles.html', {'blogs': blogs})


def blog_article(request, article_id):
    # return HttpResponse(article_id)
    article = get_object_or_404(BlogArticles, pk=article_id)
    pub = article.publish
    # return HttpResponse(type(article))
    return render(request, 'blog/content.html', {'article': article, 'publish': pub})
