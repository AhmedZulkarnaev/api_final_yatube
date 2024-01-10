from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins

from api.permissons import IsAuthorOrReadOnly
from posts.models import Group, Post
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """Управление объектами Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly,]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Создает новый объект Post и сохраняет автора."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Управление объектами Comment."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly,]

    def get_post_object_or_404(self):
        """Получает объект Post или возвращает ошибку 404."""
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        """Получает queryset комментариев объекта Post."""
        post = self.get_post_object_or_404()
        return post.comments.all()

    def perform_create(self, serializer):
        """Создает новый комментарий и сохраняет автора и связь с Post."""
        post = self.get_post_object_or_404()
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра данных о группах.
    Доступ только чтения данных о группах.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    Представление для работы с подписками пользователей.
    Поддерживает операции создания и получения списка подписчиков .
    """

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=user__username', '=following__username')

    def get_queryset(self):
        return self.request.user.followers.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
