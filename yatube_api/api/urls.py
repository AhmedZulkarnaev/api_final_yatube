from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

API_VERSION = 'v1'

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment'
)
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path(f'api/{API_VERSION}/', include('djoser.urls')),
    path(f'api/{API_VERSION}/', include('djoser.urls.jwt')),
    path(f'api/{API_VERSION}/', include(router.urls))
]
