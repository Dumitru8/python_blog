from django.contrib import admin
from blog.models import Post, Comments, Category

admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Category)
# Register your models here.
