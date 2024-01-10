from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

API_VERSION = 'v1'

router_api_v1 = DefaultRouter()
router_api_v1.register('posts', PostViewSet)
router_api_v1.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment'
)
router_api_v1.register('groups', GroupViewSet)
router_api_v1.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path(f'api/{API_VERSION}/', include('djoser.urls')),
    path(f'api/{API_VERSION}/', include('djoser.urls.jwt')),
    path(f'api/{API_VERSION}/', include(router_api_v1.urls))
]
