from django.contrib import admin
from django.urls import path

from content.views import contentServiceViewSet

urlpatterns = [
    path('content', contentServiceViewSet.as_view({
        'get':'list',
        'post':'create'
    })),
    path( 'contentfile', contentServiceViewSet.as_view({
        'post':'fileupload'
    })),
    path('content/popular', contentServiceViewSet.as_view({
        'get':'getPopularContent'
    })),
    path('content/latest', contentServiceViewSet.as_view({
        'get':'getLatestContent'
    })),
    path('content/<str:pk>', contentServiceViewSet.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'deleteContent'
    }))
    
]
