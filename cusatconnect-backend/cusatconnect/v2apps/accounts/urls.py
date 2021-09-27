from django.urls import path
from django.conf.urls import url, include

from .views import (
    UserLoginAPIView, UserRegistrationAPIView, UserListView,
    UserDeleteView, UserUpdateView, GetUserView
)

app_name = 'APP.User'

urlpatterns = [
    path('users/login/', UserLoginAPIView.as_view(), name="login"),
    path('users/user-creation/', UserRegistrationAPIView.as_view(), name="user-creation"),
    path('users/user-list/', UserListView.as_view(), name="user-list"),
    path('users/user-update/<int:pk>', UserUpdateView.as_view(), name="user-update"),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name="user-delete"),
    path('users/user-view/<int:pk>/', GetUserView.as_view(), name="user-view"),

]
