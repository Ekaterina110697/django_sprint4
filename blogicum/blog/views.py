from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import (render, redirect,
                              get_object_or_404)

from .forms import PostForm, ProfileForm, CommentForm
from .models import Post, Comment, Category
from .paginator import paginate
from .query_sets import post_query, post_query_comment, get_comment


UserClass = get_user_model()


def index(request):
    post_list = post_query_comment()
    page_obj = paginate(request, post_list)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, id):
    post = get_object_or_404(
        Post,
        pk=id
    )
    if post.author != request.user:
        post = get_object_or_404(
            post_query(),
            pk=id
        )
    form = CommentForm()
    comments = post.comments.all()
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, is_published=True, slug=category_slug
    )
    post_list = post_query_comment().filter(category=category)
    page_obj = paginate(request, post_list)
    context = {'page_obj': page_obj, 'category': category}
    return render(request, 'blog/category.html', context)


def profile(request, username):
    profile = get_object_or_404(UserClass, username=username)
    post_list = post_query_comment().filter(
        author=profile
    )
    if profile == request.user:
        post_list = get_comment().filter(
            author=profile)
    page_obj = paginate(request, post_list)
    context = {'page_obj': page_obj, 'profile': profile, }
    return render(request, 'blog/profile.html', context)


def edit_profile(request):
    instance = get_object_or_404(UserClass, username=request.user)
    form = ProfileForm(request.POST or None,
                       instance=instance)
    template_name = 'blog/user.html'
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=instance.username)
    return render(request, template_name, {'form': form})


@login_required
def create_post(request):
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    )
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        form.save()
        return redirect('blog:profile', username=request.user)
    return render(request, 'blog/create.html', {'form': form})


def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)
    if post.author != request.user:
        return redirect('blog:post_detail', id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', id)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, id):
    instance = get_object_or_404(Post,
                                 pk=id,
                                 author=request.user
                                 )
    form = PostForm(instance=instance)
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:profile', username=request.user)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def add_comment(request, id):
    post = get_object_or_404(Post, pk=id)
    if post.author != request.user:
        post = get_object_or_404(post_query(), pk=id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', id=id)


@login_required
def edit_comment(request, id, comment_id):
    comment = get_object_or_404(Comment,
                                pk=comment_id,
                                author=request.user
                                )
    form = CommentForm(request.POST or None,
                       instance=comment)
    context = {'form': form, 'comment': comment}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', id=id)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, id, comment_id):
    comment = get_object_or_404(Comment,
                                pk=comment_id,
                                post=id,
                                author=request.user
                                )
    context = {'comment': comment}
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', id=id)
    return render(request, 'blog/comment.html', context)
