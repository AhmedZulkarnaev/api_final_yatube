from django.forms import ValidationError
from rest_framework import serializers

from posts.models import Comment, Post, Follow, Group, User


class UniqueFieldsValidator:
    requires_context = True

    def __init__(self, field_names):
        self.field_names = field_names

    def __call__(self, data, serializer_field):
        values = set()
        for field_name in self.field_names:
            field_value = data.get(field_name)
            if field_value in values:
                raise ValidationError(
                    f"Значение поля '{field_name}' уже было использовано."
                )
            values.add(field_value)
        return data


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')
        read_only_fields = ('pub_date', 'author',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', 'post')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following',)

        validators = [
            UniqueFieldsValidator(['user', 'following']),
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following',),
                message='Вы уже подписаны на этого пользователя'
            )
        ]
