from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from posts.models import Follow, Group, Post, User
from .permissions import UserOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (UserOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = Post.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id is not None:
            queryset = queryset.filter(author=user_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Вы не можете изменить чужую запись.')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Вы не можете удалить чужую запись.')
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (UserOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied('Вы не можете изменять чужой комментарий.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Вы не можете удалять чужой комментарий.')
        instance.delete()


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (UserOrReadOnly, IsAuthenticated)
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def perform_create(self, serializer):
        following_username = self.request.data.get('following')
        following = User.objects.filter(username=following_username).first()
        user = self.request.user
        if not following_username:
            raise ValidationError('Отсутствует обязательное поле "following".')
        if following is None:
            raise ValidationError('Пользователь с указанным именем не найден.')
        if user.id == following.id:
            raise ValidationError('Нельзя подписаться на самого себя.')
        if Follow.objects.filter(user=user, following=following).exists():
            raise ValidationError('Вы уже подписаны на данного пользователя.')
        serializer.save(user=user, following=following)
