# Generated by Django 3.1 on 2021-07-16 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algorithmixblog', '0024_blogpostcomment_had_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
    ]
