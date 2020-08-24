
from django.urls import path
from . import views
urlpatterns = [
    path('list/', views.UserList.as_view()),
    path('user/', views.UserOne.as_view()),
    path('del/', views.UserDel.as_view()),
]
