from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from article.models import ArticlePost, Comment
from django.http import JsonResponse
from article.forms import CommentForm
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import redis
from django.conf import settings
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class PostListNew(ListView):
    template_name = 'article/posts_list.html'
    context_object_name = 'posts'
    model = ArticlePost
    paginate_by = 3

    def get_queryset(self, *args, **kwargs):
        posts = super().get_queryset()
        if 'author' in self.kwargs:
            user = User.objects.get(username=self.kwargs['author'])
            posts = posts.filter(author=user)

        for post in posts:
            view_num = r.get('article:{}:views'.format(post.pk))
            post.views = view_num.decode(encoding='utf-8') if view_num else 0
        return posts


class PostDetailNew(DetailView):
    template_name = 'article/post_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['views'] = r.incr("article:{}:views".format(self.kwargs['pk']))
        r.zincrby('posts_ranking', int(self.kwargs['pk']), 1)
        posts_ranking = r.zrange('posts_ranking', 0, -1, desc=True)[:10]
        posts_ranking_ids = [int(id) for id in posts_ranking]
        most_viewed = list(ArticlePost.objects.filter(id__in=posts_ranking_ids))
        most_viewed.sort(key=lambda x: posts_ranking_ids.index(x.id))
        context['most_viewed'] = most_viewed

        # comment form
        context['comment_form'] = CommentForm()
        return context

    def get_queryset(self, *args, **kwargs):
        article = ArticlePost.objects.filter(pk=self.kwargs['pk'], slug=self.kwargs['slug'])
        return article

    @csrf_exempt
    @require_POST
    def like_article(self):
        """ 为文章点赞 """
        # return JsonResponse({"data": dir(self)})
        pk = self.POST.get('pk')
        action = self.POST.get('action')
        if pk and action:
            try:
                post = ArticlePost.objects.get(pk=pk)
                if action == 'like':
                    post.user_like.add(self.user)
                    return JsonResponse({"code": 200,
                                         "msg": "Thanks for your support", 'count': post.user_like.all().count()})
                else:
                    post.user_like.remove(self.user)
                    return JsonResponse({"code": 200,
                                         "msg": "Anyway, we will do it better", 'count': post.user_like.all().count()})
            except:
                return JsonResponse({"code": 400, "msg": 'Error111'})
        else:

            return JsonResponse({"code": 400, "msg": 'Error2222'})

    @require_POST
    def comment(request):
        """ 文章评论　"""
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.article = ArticlePost.objects.get(pk=request.POST.get('pk'))
                new_comment.save()
                return JsonResponse({
                    "code": 200,
                    'msg': "Thanks for commenting, I will reply later.",
                    "data": {
                        'name': form.cleaned_data['commentator'],
                        'body': form.cleaned_data['body']
                    }})
            else:
                return JsonResponse({"code": 400, 'msg': "Error"})


