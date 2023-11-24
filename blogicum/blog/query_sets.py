from blog.models import Post

from django.utils import timezone
from django.db.models import Count


def get_posts_queryset(
        manager=Post.objects,
        apply_filters=True,
        with_annotation=True
):
    queryset = manager.select_related('author', 'location', 'category')
    if apply_filters:
        queryset = queryset.filter(
            is_published=True,
            pub_date__lt=timezone.now(),
            category__is_published=True
        )
    if with_annotation:
        queryset = queryset.annotate(comment_count=Count('comments'))
    return queryset.order_by('-pub_date')
