from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=64, verbose_name='Title')
    text = models.TextField(verbose_name='Text')
    created_date = models.DateTimeField(verbose_name='Created Date', auto_now_add=True)
    publish_date = models.DateTimeField(verbose_name='Publish Date', auto_now_add=True)
    published = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.title}'


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Text')
    published_date = models.DateTimeField(verbose_name='published_date', auto_now_add=True, )
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text}'


class Category(models.Model):
    text = models.CharField(max_length=52, verbose_name='Text')

    def __str__(self):
        return f'{self.text}'

class Feedback(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Text')
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(verbose_name='Rating', default=3)
    def __str__(self):
        return f'{self.text}'