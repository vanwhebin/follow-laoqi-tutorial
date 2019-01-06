from django import forms
from .models import ArticleColumn, ArticlePost, Comment


class ArticleColumnForm(forms.ModelForm):
    column = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"id": 'new_column'}))

    class Meta:
        model = ArticleColumn
        fields = ('column',)


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ('title', 'body')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('commentator', 'body')
