# Generated by Django 3.1 on 2021-07-12 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algorithmixblog', '0015_auto_20210712_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostcomment',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='blogpostcomment',
            name='updated',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]