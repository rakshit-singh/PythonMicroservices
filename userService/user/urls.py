from django.contrib import admin
from django.urls import path
from .views import UserServiceViewSet

urlpatterns = [
    path('user', UserServiceViewSet.as_view({
        'get':'list',
        'post':'create'
    })),
    path('user/<str:pk>', UserServiceViewSet.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'deleteUser'
    }))
]
