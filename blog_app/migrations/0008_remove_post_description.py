# Generated by Django 4.1.4 on 2023-01-17 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0007_post_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='description',
        ),
    ]
