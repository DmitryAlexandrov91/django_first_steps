from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('', include('blog.urls')),
    path('posts/', include('blog.urls')),
    path('category/', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('admin/', admin.site.urls),
]
