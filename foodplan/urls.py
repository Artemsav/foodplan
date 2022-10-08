from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from foodservice import views

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', render, kwargs={'template_name': 'index.html'}, name='start_page'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', render, kwargs={'template_name': 'lk.html'}, name='profile'),
    path('order/', views.get_subscription, name='order'),
    path('register/', render, kwargs={'template_name': 'registration.html'}, name='register'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
