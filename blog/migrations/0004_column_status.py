# Generated by Django 2.1.2 on 2019-02-24 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190224_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
