from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', render, kwargs={'template_name': 'index.html'}, name='start_page'),
    path('login/', render, kwargs={'template_name': 'auth.html'}, name='login_page'),
    path('lk/', render, kwargs={'template_name': 'lk.html'}, name='login_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
