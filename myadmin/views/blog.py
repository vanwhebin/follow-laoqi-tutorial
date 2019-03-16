from django.shortcuts import render, get_object_or_404, reverse
from django.http import JsonResponse
from laoqi.settings import PAGE_SIZE
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blog.models import Blog, Column, Tag, Comment
from blog.forms import BlogForm, ColumnForm, CommentForm


@login_required(login_url='/account/login/')
def blog_list(request):
    blog_qs = Blog.objects.filter(status=True)
    paginator = Paginator(blog_qs, PAGE_SIZE)
    page = request.GET.get('page')

    try:
        current_page = paginator.page(page)
        blogs = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        blogs = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        blogs = current_page.object_list

    return render(request, 'myadmin/blog/blogList.html', {'blogs': blogs, 'page': current_page})


@login_required(login_url='/account/login/')
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            blog = Blog.objects.create(
                author=request.user,
                title=cd['title'],
                body=cd['body'],
                column=cd['column']
            )
            tags = request.POST.getlist('tags[]', [])
            tag_list = []
            for tag in tags:
                tag_obj = Tag(name=tag, blog=blog)
                tag_list.append(tag_obj)
            Tag.objects.bulk_create(tag_list)
            return JsonResponse({"code": 200, 'msg': 'Created', 'url': reverse('blog:blog_detail', kwargs={"slug": blog.slug})})
        else:
            return JsonResponse({"code": 400, 'msg': 'Invalid request' + str(form.errors)})
    else:
        columns = Column.objects.all()
        return render(request, 'myadmin/blog/blog.html', {"columns": columns})


@login_required(login_url='/account/login/')
def update_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    columns = Column.objects.all()
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            blog.column = cd['column']
            blog.title = cd['title']
            blog.body = cd['body']
            blog.save()
            tags = request.POST.getlist('tags[]', [])
            tags_prev = list(Tag.objects.filter(blog=blog).values_list('name', flat=True))
            tags_add = list(set(tags).difference(set(tags_prev)))
            tags_rm = list(set(tags_prev).difference(set(tags)))
            Tag.objects.filter(name__in=tags_rm).delete()

            if tags_add:
                add_tag = []
                for add in tags_add:
                    add_tag.append(Tag(name=add, blog=blog))
                Tag.objects.bulk_create(add_tag)

            return JsonResponse({"code": 200, 'msg': 'Updated', 'url': reverse('blog:blog_detail', kwargs={"slug": blog.slug})})

    elif request.method == 'DELETE':
        blog.status = False
        blog.save()
        return JsonResponse({"code": 200, 'pk': blog.pk})

    elif request.method == 'GET':
        tags = ','.join(list(Tag.objects.filter(blog=blog).values_list('name', flat=True)))
        return render(request, 'myadmin/blog/blog.html', {"blog": blog, "columns": columns,  "tags": tags})


@login_required(login_url='/account/login')
def blog_column(request):
    column_qs = Column.objects.filter(status=True)
    lists = []
    tree = {}

    # for i in list(column_qs.values()):
    #     tree[i['id']] = i
    #
    # for l in list(column_qs.values()):
    #     obj = l
    #     if not obj['parent_id']:
    #         root = tree[obj['id']]
    #         lists.append(root)
    #     else:
    #         parent_id = obj['parent_id']
    #         if 'children' not in tree[parent_id]:
    #             tree[parent_id]['children'] = []
    #         tree[parent_id]['children'].append(tree[obj['id']])

    # print(json.dumps(lists))

    # return JsonResponse(lists, safe=False)

    return render(request, 'myadmin/column/list.html', {'columns': column_qs})


@login_required(login_url='/account/login')
def update_column(request, pk):
    column = get_object_or_404(Column, pk=pk)
    if request.method == 'POST':
        form = ColumnForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            column.column = cd['column']
            column.parent = cd['parent']
            column.save()
            return JsonResponse({"code": 200, 'msg': 'Updated', 'pk': column.pk})

    elif request.method == 'DELETE':
        column.status = False
        column.save()
        return JsonResponse({"code": 200, 'pk': column.pk})


@login_required(login_url='/account/login')
def create_column(request):
    if request.method == 'POST':
        form = ColumnForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"code": 200, 'msg': 'Created'})
        else:
            return JsonResponse({"code": 400, 'msg': 'Invalid request' + str(form.errors)})


@login_required(login_url='/account/login')
def comment_list(request):
    comment_qs = Comment.objects.all().exclude(commentator=request.user).order_by('-create_time', 'replied')
    paginator = Paginator(comment_qs, PAGE_SIZE)
    page = request.GET.get('page')

    try:
        current_page = paginator.page(page)
        comments = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        comments = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        comments = current_page.object_list

    # return JsonResponse({"data": comments})
    # return render(request, 'myadmin/comment/list.html', {'comments': comments, 'page': current_page})
    return render(request, 'myadmin/comment/comment_inbox.html', {'comments': comments, 'page': current_page})


def reply_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.status = True
        comment.replied = True
        comment.save()
        Comment.objects.create(commentator=request.user.username,
                               email=request.user.email,
                               blog=comment.blog,
                               status=True,
                               body=request.POST.get('body'))
        return JsonResponse({"code": 200})
    elif request.method == 'DELETE':
        comment.delete()
        return JsonResponse({'code': 200,  'pk': comment.pk})




