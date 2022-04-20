from rest_framework import serializers

from .models import Category, Topic, Replies, User, Created


class TopicUnSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')

    class Meta:
        model = Topic
        fields = (
            'id', 'name', 'url', 'author', 'category',
            'created', 'content', 'tags'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'author', 'created')


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('name',  'url', 'author', 'created', 'content', 'tags')


class RepliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Replies
        fields = ('author_name', 'content',  'created', 'updated', 'parent')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'image')


class CreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Created
        fields = ('topic',)















