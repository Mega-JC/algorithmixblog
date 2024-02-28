# Generated by Django 3.1 on 2021-07-13 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('algorithmixblog', '0019_auto_20210713_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpostcomment',
            name='favorers',
            field=models.ManyToManyField(blank=True, related_name='favorite_blogposts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogposts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='likers',
            field=models.ManyToManyField(blank=True, related_name='liked_blogposts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='related_blogposts', to='algorithmixblog.BlogPostTag'),
        ),
        migrations.AlterField(
            model_name='blogpostcomment',
            name='likers',
            field=models.ManyToManyField(blank=True, related_name='liked_blogpost_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserFavorites',
        ),
    ]