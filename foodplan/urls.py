from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from subscription import views as subs_views
from foodservice import views as fs_views

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', render, kwargs={'template_name': 'index.html'}, name='start_page'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', fs_views.get_account, name='profile'),
    path('order/', subs_views.get_subscription, name='order'),
    path('register/', fs_views.register_user, name='register'),
    path('recipes/', fs_views.get_recipes, name='resipes'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
