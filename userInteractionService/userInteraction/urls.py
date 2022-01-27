from django.contrib import admin
from django.urls import path

from .views import ContentView, UserView, InternalInteractionViewSet, ReadServiceViewSet, LikeServiceViewSet

urlpatterns = [
    path('like', LikeServiceViewSet.as_view({
        'get':'list',
        'put':'update'
    })),
    path('read', ReadServiceViewSet.as_view({
        'get':'list',
        'put':'update'
    })),
    path('interactions', InternalInteractionViewSet.as_view({
        'get':'getInteractions'
    })),
    path('user', UserView.as_view({
        'post':'createUser',
        'delete':'deleteUser'
    })),
    path('user/<str:user_id>', UserView.as_view({
        'delete':'deleteUser'
    })),
    path('content/<str:contentTitle>', ContentView.as_view({
        'delete':'deleteContent'
    }))
]
