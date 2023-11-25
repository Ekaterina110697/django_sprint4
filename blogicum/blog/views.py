from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.shortcuts import (render, redirect,
                              get_object_or_404)
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView

from .forms import PostForm, ProfileForm, CommentForm
from .models import Post, Comment, Category
from .paginator import paginate
from .query_sets import get_posts_queryset


class RegistrationView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('pages:about')


UserClass = get_user_model()


def index(request):
    post_list = get_posts_queryset(apply_filters=True,
                                   with_annotation=True)
    page_obj = paginate(request, post_list)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(
        get_posts_queryset(apply_filters=False, with_annotation=False),
        pk=post_id)
    if post.author != request.user and not (
            post.is_published
            and post.category.is_published
            and post.pub_date <= timezone.now()
    ):
        raise Http404('Страница не существует')
    form = CommentForm()
    comments = post.comments.all()
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, is_published=True, slug=category_slug
    )
    post_list = get_posts_queryset(manager=category.posts,
                                   apply_filters=True,
                                   with_annotation=True)
    page_obj = paginate(request, post_list)
    context = {'page_obj': page_obj, 'category': category}
    return render(request, 'blog/category.html', context)


def profile(request, username):
    profile = get_object_or_404(UserClass, username=username)
    if profile == request.user:
        post_list = get_posts_queryset(manager=profile.posts,
                                       apply_filters=False,
                                       with_annotation=True)
    else:
        post_list = get_posts_queryset(manager=profile.posts,
                                       apply_filters=True,
                                       with_annotation=True)
    page_obj = paginate(request, post_list)
    context = {'page_obj': page_obj, 'profile': profile, }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    instance = request.user
    form = ProfileForm(request.POST or None,
                       instance=instance)
    template_name = 'blog/user.html'
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=instance.username)
    return render(request, template_name, {'form': form})


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'blog/create.html', {'form': form})
    new_post = form.save(commit=False)
    new_post.author = request.user
    new_post.save()

    return redirect('blog:profile', username=request.user)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, post_id):
    instance = get_object_or_404(Post, pk=post_id, author=request.user)
    form = PostForm(instance=instance)
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:profile', username=request.user)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        post = get_object_or_404(get_posts_queryset(), pk=post_id)
    form = CommentForm(request.POST)
    if not form.is_valid():
        return render(request, 'blog/create.html', {'form': form})
    comment = form.save(commit=False)
    comment.author = request.user
    comment.post = post
    comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment,
                                pk=comment_id,
                                post_id=post_id,
                                author=request.user)
    form = CommentForm(request.POST or None, instance=comment)
    context = {'form': form, 'comment': comment}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment,
                                pk=comment_id,
                                post_id=post_id,
                                author=request.user)
    context = {'comment': comment}
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', context)
