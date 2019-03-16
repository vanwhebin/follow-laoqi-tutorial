# Generated by Django 2.1.2 on 2019-02-23 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('slug', models.SlugField(default='', max_length=100)),
                ('body', models.TextField(blank=True, default='', max_length=5000)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('reads', models.PositiveIntegerField(blank=True, default=1)),
                ('likes', models.PositiveIntegerField(blank=True, default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column', models.CharField(blank=True, default='', max_length=100)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('create_time',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentator', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='blog.Blog')),
            ],
            options={
                'ordering': ('create_time',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag', to='blog.Blog')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='column',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='blog.Column'),
        ),
    ]
