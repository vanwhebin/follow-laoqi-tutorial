# Generated by Django 2.1.2 on 2019-01-06 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('create_time',)},
        ),
    ]
