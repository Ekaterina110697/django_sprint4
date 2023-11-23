from django.urls import include, path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'profile_edit/',
        views.edit_profile,
        name='edit_profile'
    ),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:id>/', include([
        path('edit/', views.edit_post, name='edit_post'),
        path('delete/', views.delete_post, name='delete_post'),
        path('comment/', views.add_comment, name='add_comment'),
        path('edit_comment/<int:comment_id>/',
             views.edit_comment, name='edit_comment'),
        path('delete_comment/<int:comment_id>/',
             views.delete_comment, name='delete_comment'),
        path('', views.post_detail, name='post_detail'),
    ])),
    path(
        'profile/<slug:username>/',
        views.profile,
        name='profile'
    ),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts'
    )
]
