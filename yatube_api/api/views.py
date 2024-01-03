from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from posts.models import Comment, Follow, Group, Post
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer)


class AuthorPermissionMixin:
    """Mixin для проверки доступа автора к объектам."""

    def handle_author_permission(self, instance, request):
        """Проверяет доступ автора к объекту."""
        if request.user != instance.author:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        """Обновляет объект и проверяет доступ автора."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        response = self.handle_author_permission(instance, request)
        if not response:
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        return (
            response
            or Response(serializer.data, status=status.HTTP_200_OK)
        )

    def destroy(self, request, *args, **kwargs):
        """Удаляет объект и проверяет доступ автора."""
        instance = self.get_object()
        response = self.handle_author_permission(instance, request)
        if not response:
            instance.delete()
        return (
            response or Response(status=status.HTTP_204_NO_CONTENT)
        )


class PostViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    """Управление объектами Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Создает новый объект Post и сохраняет автора."""
        serializer.save(author=self.request.user)


class CommentViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    """Управление объектами Comment."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FollowViewSet(viewsets.ViewSet):
    """
    ViewSet для управления подписками пользователей.
    Позволяет просматривать и создавать подписки.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Follow.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        """
        Получает список подписок текущего пользователя.
        """
        return self.queryset.filter(user=self.request.user)

    def list(self, request):
        """
        Показывает список подписок пользователя
        с возможностью фильтрации по имени пользователя.
        """
        search_param = request.GET.get('search')
        queryset = self.get_queryset()

        if search_param:
            queryset = queryset.filter(
                following__username__icontains=search_param)

        serializer = FollowSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Создает новую подписку пользователя на другого пользователя.
        """
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
