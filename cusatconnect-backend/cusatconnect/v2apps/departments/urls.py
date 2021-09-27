from django.urls import path
from .views import DepView, StreamView

urlpatterns = [
    path('users/stream/', StreamView.as_view(), name="stream"),
    path('users/dept/<int:pk>/', DepView.as_view(), name="dept"),
]
