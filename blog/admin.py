from django.contrib import admin
from .models import Blog, BlogType, ReadNum


# 后台显示
# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'blog_type', 'read_count', 'created_time', 'update_time')


@admin.register(BlogType)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')
    # ordering = ('-id')


@admin.register(ReadNum)
class ReadNnmAdmin(admin.ModelAdmin):
    list_display = ('count', 'blog')

