# Generated by Django 2.1.2 on 2019-02-24 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_column_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commentator',
            field=models.EmailField(max_length=100),
        ),
    ]
