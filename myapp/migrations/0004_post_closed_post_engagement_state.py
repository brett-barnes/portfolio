# Generated by Django 5.0.7 on 2024-08-19 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_comment_post_comments_reply_comment_replies'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='engagement_state',
            field=models.CharField(default='zero', max_length=40),
        ),
    ]