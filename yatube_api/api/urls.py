from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, GroupViewSet

API_VERSION = 'v1'

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)
router.register('groups', GroupViewSet)

urlpatterns = [
    path(f'api/{API_VERSION}/', include(router.urls))
]
