from blog.models import Post

from django.utils import timezone
from django.db.models import Count


def post_query():
    return Post.objects.select_related(
        'category',
        'location',
        'author',
    ).only(
        'title',
        'text',
        'pub_date',
        'author__username',
        'category__title',
        'category__slug',
        'location__name',
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )


def post_query_comment():
    posts = annotation(post_query())
    return posts


def get_comment():
    comment_number = annotation(Post.objects.all())
    return comment_number


def annotation(queryset):
    posts_with_comments = queryset.annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')
    return posts_with_comments
