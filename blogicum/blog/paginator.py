from blogicum.settings import POSTS_ON_PAGE
from django.core.paginator import Paginator


def paginate(request, post_list):
    paginator = Paginator(post_list, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
