from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Blog
from .models import Comment
from .forms import CommentForm


# Create your views here.

def blog_comment(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)  # 找到具体的博客
    if request.method == 'POST':
        form = CommentForm(request.POST)  # request.POST 获得前端表单提交的数据
        # 根据这些数据,生成一个表单对象
        if form.is_valid():  # 表单对象是否合法
            # form的 save函数,会直接保存数据到数据库
            comment = form.save(commit=False)  # 生成一个comment对象,commit暂时未提交
            comment.blog = blog  # 将博客与评论关联起来
            comment.save()

            # redirect,重新定向,接收一个模型的实例对象(Blog)
            # 它会自动调用这个模型的get_absolute_url方法
            # 这个方法会返回一个地址
            return redirect(blog)



        else:  # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误
            comment_list = Comment.objects.filter(blog=blog)  # 其作用是获取这篇 blog 下的的全部评论，
            content = {'blog': blog,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog_detail.html', context=content)
            # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。

    return redirect(blog)
