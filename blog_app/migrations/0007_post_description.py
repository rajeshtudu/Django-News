# Generated by Django 4.1.4 on 2023-01-17 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0006_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
