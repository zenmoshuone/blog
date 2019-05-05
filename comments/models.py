from django.db import models
from blog.models import Blog

# Create your models here.
class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    blog = models.ForeignKey(Blog,on_delete=models.DO_NOTHING)  # 外键关联Blog 1对多

    def __str__(self):
        return self.text[:10]  # 显示前10个
