# Generated by Django 5.0.4 on 2024-05-06 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_post_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='dislike',
        ),
    ]