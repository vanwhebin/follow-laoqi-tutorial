from django import forms
from .models import Blog, Column, Comment


class BlogForm (forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('title', 'body', 'column')


class ColumnForm(forms.ModelForm):

    class Meta:
        model = Column
        fields = ('column', 'parent')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('commentator', 'body', 'email')
