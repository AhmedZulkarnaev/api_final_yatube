from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from posts.models import Post, Comment, Group
from .serializers import PostSerializer, CommentSerializer, GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_post_object_or_404(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        post = self.get_post_object_or_404()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post_object_or_404()
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]