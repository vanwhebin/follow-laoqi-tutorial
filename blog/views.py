from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blog.forms import CommentForm
from blog.models import Blog, Comment, Tag
from laoqi.settings import PAGE_SIZE
from django.http import JsonResponse


def blog_list(request):
    blog_qs = Blog.objects.filter(status=True)
    paginator = Paginator(blog_qs, PAGE_SIZE)
    page = request.GET.get('page', 1)

    try:
        current_page = paginator.page(page)
        blogs = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        blogs = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        blogs = current_page.object_list
    return render(request, 'blog/list.html', {"blogs": blogs, "page": current_page})


def blog_article(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    blog.reads = blog.reads + 1
    blog.save()
    pub = blog.publish
    comments = Comment.objects.filter(blog=blog, status=True).order_by('create_time')
    tags = Tag.objects.filter(blog=blog).values_list('name', flat=True)
    related = Blog.objects.filter(column=blog.column)[:5]
    data = {'article': blog, 'publish': pub, "comments": comments, "tags": tags, "related": related}
    return render(request, 'blog/detail.html', data)


def comment_article(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['commentator'] = cd['commentator'].replace('script', '')
            cd['body'] = cd['body'].replace('script', '')
            Comment.objects.create(blog=blog, commentator=cd['commentator'], body=cd['body'], email=cd['email'])
            return JsonResponse({"code": 200})
        else:
            return JsonResponse({"code": 400, 'msg': str(form.errors)})



