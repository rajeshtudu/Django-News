from django.contrib import admin

from blog_app.models import Category, Comment, NewsLetter, Post, Tag

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(NewsLetter)
admin.site.register(Comment)
