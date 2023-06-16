from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from blog.models import Post, Comments, Category, Feedback
from blog.forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.all().filter(published=True)
    category = Category.objects.all()
    counter = posts.count()
    return render(request, 'blog/post_list.html', {'items': posts, 'category': category, 'counter': counter})


def post_draft(request):
    posts = Post.objects.all().filter(published=False)
    category = Category.objects.all()
    counter = posts.count()
    return render(request, 'blog/post_list.html', {'items': posts,
                                                   'category': category,
                                                   'counter': counter})


def published_post(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    post.published = True
    post.save()
    return render(request, 'blog/post_detail.html', {'post': post})


def rating(post_pk):
    fb = Feedback.objects.filter(post=post_pk)
    count = sum([i.rating for i in fb]) / fb.count()
    return round(count, 1)


def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comments = Comments.objects.filter(post=post_pk)
    counter = comments.count()
    rate = rating(post_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.published_date = datetime.now()
            comment.save()
            return redirect('post_detail', post_pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'comments': comments,
                                                     'counter': counter,
                                                     'comment_form': comment_form,
                                                     'rating': rate})


def post_new(request):
    if request.method == "GET":
        form = PostForm
        category = Category.objects.all()
        return render(request, 'blog/post_new.html', {'form': form, 'category': category})
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_date = datetime.now()
            post.publish_date = datetime.now()
            post.save()
            return redirect('post_detail', post_pk=post.pk)


def post_edit(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "GET":
        form = PostForm(instance=post)
        return render(request, 'blog/post_new.html', {'form': form})
    else:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_date = datetime.now()
            post.publish_date = datetime.now()
            post.save()
            return redirect('post_detail', post_pk=post.pk)


def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk).delete()
    return redirect('post_list')


def categories(request, category_pk):
    posts = Post.objects.filter(category=category_pk)
    category = Category.objects.all()
    return render(request, 'blog/post_list.html', {'items': posts, 'category': category})


def delete_comments(request, post_pk, comment_pk):
    post = Post.objects.get(pk=post_pk)
    comment = get_object_or_404(Comments, pk=comment_pk).delete()
    return redirect('post_detail', post_pk=post.pk)

def feedback(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    fb = Feedback.objects.filter(post=post_pk)
    context = {'fb': fb, 'post': post}
    return render(request, 'blog/feedback.html', context)

