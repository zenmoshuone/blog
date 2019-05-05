from django.shortcuts import render, get_object_or_404
from .models import BlogType, Blog
from django.core.paginator import Paginator
import markdown
from django.db.models import Count


def contrl(request,blogs):
    page_num = request.GET.get('page', 1)  # 获得s? 后面字典的内容(都是字符串)，如果没有，默认为第一页
    p = Paginator(blogs, 3)  # 把所有文章进行分页，每页5个
    page = p.get_page(page_num)  # 如果输入的:rpae_num 是非数字(不合法),会直接返回第一页,如果大于总页面，会返回最后一页
    page_nums = p.num_pages  # 获得一共有多少页
    courrent_page_num = page.number  # page.number 获得当前的页码
    page_range = list(range(max(1, courrent_page_num - 2), courrent_page_num)) + \
                 list(range(courrent_page_num, min(courrent_page_num + 2, page_nums) + 1))  # 显示的页码
    # 显示的页码下标为0的值
    if page_range[0] - 1 > 2:
        page_range.insert(0, '...')
    if page_nums - page_range[-1] > 2:
        page_range.append('...')
    # 显示的第一个页码不为1时在下标0中插入第一个页码,显示的最后一个页码不为最大页码是追加最后一个页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != page_nums:
        page_range.append(page_nums)

    context = {}
    context['date_list'] = Blog.objects.dates('created_time', 'month', order='DESC')
    context['page_range'] = page_range
    types = BlogType.objects.all()  # 查找所有的分类
    context['page'] = page
    # context['blogs'] = blogs

    # 第一种 统计博客分类有多少篇 要修改为
    # type_list = []
    # for type in types:
    #     type.blog_count = Blog.objects.filter(blog_type=type).count()
    #     type_list.append(type)
    # 第二种 统计博客分类有多少篇 要修改为
    type_list = BlogType.objects.annotate(blog_count=Count('blog'))
    # annotate在这里的作用是,给BlogType临时添加一个叫做blog_count(随便取名字)的属性
    # Count中的参数是:指BlogType想关联的外键的模型类,使用的是定义外键时,设置的related_name的值,related_name的默认值其实是
    # 第三种 统计博客分类有多少篇 type.blog_set 反向获取相关联外键模型
    # 第三种要修改为 context['types'] = types 并且blog_list.html中({{ type.blog_count }})修改为({{ type.blog_set.count }})

    context['types'] = type_list

    return context


# Create your views here.
def blog_list(request):
    # 列表页
    blogs = Blog.objects.all()  # 查找所有的博客文章
    page_num = request.GET.get('page', 1)  # 获得s? 后面字典的内容(都是字符串)，如果没有，默认为第一页
    p = Paginator(blogs, 3)  # 把所有文章进行分页，每页5个
    page = p.get_page(page_num)  # 如果输入的:rpae_num 是非数字(不合法),会直接返回第一页,如果大于总页面，会返回最后一页
    page_nums = p.num_pages  # 获得一共有多少页
    courrent_page_num = page.number  # page.number 获得当前的页码
    page_range = list(range(max(1, courrent_page_num - 2), courrent_page_num)) + \
                 list(range(courrent_page_num, min(courrent_page_num + 2, page_nums) + 1))  # 显示的页码
    # 显示的页码下标为0的值
    if page_range[0] - 1 > 2:
        page_range.insert(0, '...')
    if page_nums - page_range[-1] > 2:
        page_range.append('...')
    # 显示的第一个页码不为1时在下标0中插入第一个页码,显示的最后一个页码不为最大页码是追加最后一个页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != page_nums:
        page_range.append(page_nums)

    context = {}
    context['date_list'] = Blog.objects.dates('created_time','month',order='DESC')
    context['page_range'] = page_range
    types = BlogType.objects.all()  # 查找所有的分类
    context['page'] = page
    # context['blogs'] = blogs

    # 第一种 统计博客分类有多少篇 要修改为
    # type_list = []
    # for type in types:
    #     type.blog_count = Blog.objects.filter(blog_type=type).count()
    #     type_list.append(type)
    # 第二种 统计博客分类有多少篇 要修改为
    type_list = BlogType.objects.annotate(blog_count=Count('blog'))
    # annotate在这里的作用是,给BlogType临时添加一个叫做blog_count(随便取名字)的属性
    #Count中的参数是:指BlogType想关联的外键的模型类,使用的是定义外键时,设置的related_name的值,related_name的默认值其实是
    # 第三种 统计博客分类有多少篇 type.blog_set 反向获取相关联外键模型
    # 第三种要修改为 context['types'] = types 并且blog_list.html中({{ type.blog_count }})修改为({{ type.blog_set.count }})



    context['types'] = type_list
    return render(request, 'blog_list.html', context=context)
    # render 1.将从数据库中查找到的数据，以字典context 交给它的第二个参数
    # 2.将第二个参数，渲染好的内容，返回给调用者


def blog_detail(request, id):
    # 详情页
    blog = get_object_or_404(Blog, pk=id)
    # 内容输入可以使用markdown
    blog.content = markdown.markdown(blog.content, exetnsions={
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    })

    # previous_blog 上一篇 , created_time__gt(大于当前时间) , blog.created_time(当前时间) ,last()最后的一个.(时间排序是最新的在上面)
    previous_blog = Blog.objects.filter(created_time__gt=blog.created_time).last()
    # next_blog 下一篇 , created_time__lt(小于当前时间) , blog.created_time(当前时间) frist() 第一个.(时间排序是以前的在下面)
    next_blog = Blog.objects.filter(created_time__lt=blog.created_time).first()


    context = {}

    context['blog'] = blog
    context['previous_blog'] = previous_blog
    context['next_blog'] = next_blog
    return render(request, 'blog_detail.html', context=context)


def blog_type(request, type_id):
    # 电影类型分类页
    blog_type = get_object_or_404(BlogType, pk=type_id)
    page_num = request.GET.get('page', 1)  # 获得s? 后面字典的内容(都是字符串)，如果没有，默认为第一页

    types = BlogType.objects.all()
    blogs = Blog.objects.filter(blog_type=blog_type)
    p = Paginator(blogs, 3)  # 把所有文章进行分页，每页5个
    page = p.get_page(page_num)  # 如果输入的:rpae_num 是非数字(不合法),会直接返回第一页,如果大于总页面，会返回最后一页

    page_nums = p.num_pages  # 获得一共有多少页
    # 获得当前的页码
    current_page_num = page.number

    page_range = list(range(max(1, current_page_num - 2), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, page_nums) + 1))
    if page_range[0] - 1 > 2:
        page_range.insert(0, '...')
    if page_nums - page_range[-1] > 2:
        page_range.append('...')

    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != page_nums:
        page_range.append(page_nums)

    type_list = BlogType.objects.annotate(blog_count=Count('blog'))
    context = {}
    context['page_range'] = page_range
    context['page'] = page
    # context['blogs'] = blogs
    context['types'] = type_list
    context['blog_type'] = blog_type
    context['date_list'] = Blog.objects.dates('created_time', 'month', order='DESC')
    return render(request, 'blog_type.html', context=context)


def index(request):
    # 首页
    return render(request, 'index.html')


def blog_date(request,year,month):
    # 日期归档
    blogs = Blog.objects.filter(created_time__year=year,created_time__month=month)  # 日期归档 筛选出同年同月的博客放在一起
    page_num = request.GET.get('page', 1)  # 获得s? 后面字典的内容(都是字符串)，如果没有，默认为第一页
    p = Paginator(blogs, 3)  # 把所有文章进行分页，每页3个
    page = p.get_page(page_num)  # 如果输入的:rpae_num 是非数字(不合法),会直接返回第一页,如果大于总页面，会返回最后一页
    page_nums = p.num_pages  # 获得一共有多少页
    courrent_page_num = page.number  # page.number 获得当前的页码
    page_range = list(range(max(1, courrent_page_num - 2), courrent_page_num)) + \
                 list(range(courrent_page_num, min(courrent_page_num + 2, page_nums) + 1))  # 显示的页码
    # 显示的页码下标为0的值减1大于2时在下标0中插入'...'的一个页码
    #最大页码-显示的页码最后一页大于2时，追加一个'...'的一个页码
    if page_range[0] - 1 > 2:
        page_range.insert(0, '...')
    if page_nums - page_range[-1] > 2:
        page_range.append('...')
    # 显示的第一个页码不为1时在下标0中插入第一个页码,显示的最后一个页码不为最大页码是追加最后一个页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != page_nums:
        page_range.append(page_nums)

    context = {}
    context['date_list'] = Blog.objects.dates('created_time', 'month', order='DESC')  # 日期归档 以月份进行排序,最新的在前面
    context['page_range'] = page_range
    types = BlogType.objects.all()  # 查找所有的分类
    context['page'] = page

    type_list = BlogType.objects.annotate(blog_count=Count('blog'))

    context['types'] = type_list
    context['date_info'] = f'{year}年{month}月'  # 日期归档 显示年月份
    return render(request,'blog_date.html',context=context)
