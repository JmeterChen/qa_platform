from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', include('index.urls')),
    path('tapd/', include('tapd.urls')),
    path('api/v1/problem_guide/', include('problem_guide.urls')),
    path('user/', include('user.urls')),
    re_path('^api/v1/', include("mypro.urls")),
    re_path('^api/v1/', include('qualitydata.urls')),
    re_path('^api/v1/', include("testcase.urls")),
    re_path('^api/v1/', include("user.urls")),
    re_path('^api/v1/', include("tapd.urls")),
]
