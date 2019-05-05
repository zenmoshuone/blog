from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# 类似数据库表

# Create your models here.
class BlogType(models.Model):
    # 文章分类
    type_name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.type_name}'


class Blog(models.Model):
    # 博客
    title = models.CharField(max_length=50)  # 文章标题
    content = models.TextField()  # 文章内容
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # 文章作者 ,外键 1对多
    created_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(auto_now=True)  # 修改时间
    # related_name='blog' 这个是默认添加的
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING, related_name='blog')  # 文章分类

    # read_num = models.IntegerField(default=0)  # 博客阅读次数,默认值为0

    def __str__(self):
        return f'{self.title}'

    def read_count(self):  # 后台显示阅读次数
        try:
            return self.readnum.count  # 显示阅读次数 ,ReadNum的小写
        except:
            return 0  # 没有阅读次数显示0

    def get_absolute_url(self):  # 评论提交
        # 返回到'detail' 页面
        return reverse('detail', kwargs={'id': self.pk})

    class Meta:
        # 以发布时间对Blog垒进行排序
        ordering = [
            # ('-' 号 最新的放在最前面)
            '-created_time'
        ]


class ReadNum(models.Model):
    count = models.IntegerField(default=0)  # 博客阅读次数,默认值为0
    blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING)  # 外键 1对1
