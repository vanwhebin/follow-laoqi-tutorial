from django.shortcuts import render, get_object_or_404, reverse
from article.models import ArticleColumn, ArticlePost
from django.contrib.auth.decorators import login_required
from article.forms import ArticleColumnForm, ArticlePostForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='/account/login/')
def article_column(request):
    if request.method == "POST":
        form = ArticleColumnForm(request.POST)
        if form.is_valid():
            if ArticleColumn.objects.filter(user=request.user, column=request.POST.get('column').strip()):
                return JsonResponse({"code": 400, "msg": "栏目名已存在"})
            else:
                ArticleColumn.objects.create(
                    user=request.user,
                    column=form.cleaned_data['column']
                )
                return JsonResponse({"code": 200, 'msg': "Created"})
        else:
            return JsonResponse({"code": 400, "msg": str(form.errors)})
    elif request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        form = ArticleColumnForm()
        return render(request, 'article/article_column.html', {'columns': columns, 'form': form})


@login_required(login_url='/account/login/')
def edit_article_column(request, pk):
    article_col = get_object_or_404(ArticleColumn, pk=pk)
    if request.method == "POST":
        form = ArticleColumnForm(request.POST)
        if form.is_valid():
            article_col.column = form.cleaned_data['column']
            article_col.save()
            return JsonResponse({"code": 200, "msg": "Updated"})
        else:
            return JsonResponse({"code": "400", "msg": str(form.errors)})
    elif request.method == 'DELETE':
        article_col.delete()
        return JsonResponse({"code": 200, "msg": "Deleted"})


@csrf_exempt
@require_POST
def del_article_column(request, pk):
    article_col = get_object_or_404(ArticleColumn, pk=pk)
    article_col.delete()
    return JsonResponse({"code": 200, "msg": "Deleted"})


@login_required(login_url='/account/login/')
def article_post(request):
    if request.method == "POST":
        form = ArticlePostForm(request.POST)
        if form.is_valid():
            res = ArticlePost.objects.create(
                author=request.user,
                title=request.POST.get('title').strip(),
                column=ArticleColumn.objects.get(pk=request.POST.get('column').strip()),
                body=request.POST.get('body').strip()
            )
            return JsonResponse({'code': 200,  'url': reverse('article:article_detail', args=[res.id, res.slug])})
        else:
            return JsonResponse({"code": 400, "error": form.errors})
    elif request.method == "GET":
        form = ArticlePostForm()
        article_col = request.user.article_column.all()
        return render(request, 'article/article_post.html', {'article_column': article_col, 'form': form})


@login_required(login_url='/account/login/')
def article_list(request):
    articles = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request, 'article/article_list.html', {'posts': articles, 'page': current_page})


def post_list(request):
    articles = ArticlePost.objects.all()
    paginator = Paginator(articles, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request, 'article/posts_list.html', {'posts': articles, 'page': current_page})


@login_required(login_url='/account/login')
def edit_article_post(request, pk):
    post = get_object_or_404(ArticlePost, pk=pk)
    if request.method == 'POST':
        form = ArticlePostForm(request.POST)
        if form.is_valid():
            post.body = request.POST.get('body').strip()
            post.title = request.POST.get('title').strip()
            post.column = ArticleColumn.objects.get(pk=request.POST.get('column').strip())
            post.save()
            return JsonResponse({
                "code": 200,
                "msg": 'Updated',
                'url': reverse('article:article_detail', args=[post.id, post.slug])
            })
        else:
            return JsonResponse({"code": 400, "msg": str(form.errors)})

    elif request.method == 'GET':
        article_col = request.user.article_column.all()
        return render(request, 'article/edit_article_post.html', {"post": post, 'article_column': article_col})
    else:
        post.delete()
        return JsonResponse({"code": 200, 'msg': "Deleted"})


@login_required(login_url='/account/login')
def def_article_post(request, pk):
    post = get_object_or_404(ArticlePost, pk=pk)
    post.delete()
    return JsonResponse({"code": 200, 'msg': 'Delete'})


@login_required(login_url='/account/login')
def article_detail(request, pk, slug):
    article = get_object_or_404(ArticlePost, id=pk, slug=slug)
    return render(request, 'article/post_detail.html', {'article': article})
