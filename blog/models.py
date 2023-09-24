import markdown
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags


# Category: 分类
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# Tag: 标签
class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章
class Post(models.Model):
    # 文章标题
    title = models.CharField('标题', max_length=70)
    # 文章正文
    body = models.TextField('正文')
    # 文章创建时间、最后一次修改时间。创建时间字段的值将由系统自动获取
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    # 文章摘要
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    # 分类 & 标签：
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    # 文章作者/User是django内置/这里同样是一对多的关系，一个作者可能会有多篇文章
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"title: {self.title}, author: {self.author}, created_time: {self.created_time}"

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        # 自动生成摘要：将markdown文本转换为HTML文本，注意需要去掉文本中的HTML标签
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
