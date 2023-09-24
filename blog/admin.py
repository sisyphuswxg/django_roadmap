from django.contrib import admin

from .models import Post, Category, Tag


class PostAdmin(admin.ModelAdmin):
    # 控制Post列表页展示的字段
    list_display = ['title', 'created_time', 'modified_time', 'category', 'display_tags', 'author']
    # 控制表单展示的字段：
    fields = ['title', 'body', 'excerpt', 'category', 'tag']

    # 重写display_tags方法，用于展示多对多字段 -> tag
    def display_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tag.all()])

    display_tags.short_description = '标签'

    # 重写save_model方法，将当前登录的用户赋值给Post的author字段
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
