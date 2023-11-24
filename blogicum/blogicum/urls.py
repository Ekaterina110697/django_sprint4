from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from blog.views import RegistrationView

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

urlpatterns = [
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        RegistrationView.as_view(),
        name='registration',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
