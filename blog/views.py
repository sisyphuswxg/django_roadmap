from django.db.models.functions import TruncMonth
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from blog.models import Post, Category, Tag

from datetime import timedelta, datetime
import markdown
import re


# def index(request):
#     return HttpResponse("欢迎访问我的博客首页！")

# def index(request):
#     return render(request, 'blog/index.html', context={
#         'title': '我的博客主页',
#         'welcome': '欢迎访问我的博客主页'
#     })

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'index.html', context={'post_list': post_list})


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'detail.html', context={'post': post})


# 增加markdown功能：
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',  # 基础扩展
        'markdown.extensions.codehilite',  # 语法高亮扩展
        'markdown.extensions.toc',  # 自动生成目录
    ])
    post.body = md.convert(post.body)

    # 对toc处理：只有在文章存在目录结构时，才显示侧边栏的目录结构 #   -> 正则表达式来测试ul标签中是否包含元素来确定是否存在目录
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(
        1) if m is not None else ''  # post实例本身是没有toc属性的，这里是动态给它加上了toc这个属性 - Python动态语言
    return render(request, 'detail.html', context={'post': post})


def archive(request, year, month):
    # 获取指定日期的前后一个月的日期
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'index.html', context={'post_list': post_list})


def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tag=t).order_by('-created_time')
    return render(request, 'index.html', context={'post_list': post_list})
