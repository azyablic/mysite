from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.user_login, name="login" ),
    path('logout/', views.user_logout),
    path('registration/', views.user_registration, name="registration"),
    path('', include('notebook.urls')),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)