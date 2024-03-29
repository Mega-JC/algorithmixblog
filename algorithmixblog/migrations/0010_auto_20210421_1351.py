# Generated by Django 3.1 on 2021-04-21 11:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algorithmixblog', '0009_auto_20210420_2207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfavorites',
            name='algo_struct_posts',
        ),
        migrations.RemoveField(
            model_name='userfavorites',
            name='blog_posts',
        ),
        migrations.AddField(
            model_name='userfavorites',
            name='fav_algstr_posts',
            field=models.ManyToManyField(blank=True, related_name='user_favorite_list', to='algorithmixblog.AlgoStructPost'),
        ),
        migrations.AddField(
            model_name='userfavorites',
            name='fav_blog_posts',
            field=models.ManyToManyField(blank=True, related_name='user_favorite_list', to='algorithmixblog.BlogPost'),
        ),
        migrations.AlterField(
            model_name='algostructpost',
            name='downvoters',
            field=models.ManyToManyField(blank=True, related_name='downvoted_algstr_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='algostructpost',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='related_algstr_posts', to='algorithmixblog.AlgoStructPostTag'),
        ),
        migrations.AlterField(
            model_name='algostructpost',
            name='upvoters',
            field=models.ManyToManyField(blank=True, related_name='upvoted_algstr_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
