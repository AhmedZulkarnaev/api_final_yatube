from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowtViewSet

API_VERSION = 'v1'

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)
router.register('groups', GroupViewSet)
router.register('follow', FollowtViewSet)

urlpatterns = [
    path(f'api/{API_VERSION}/', include(router.urls))
]
