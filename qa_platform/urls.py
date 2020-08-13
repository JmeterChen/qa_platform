from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', include('index.urls')),
    path('tapd/', include('tapd.urls')),
    re_path('^api/v1/', include("mypro.urls")),
]
