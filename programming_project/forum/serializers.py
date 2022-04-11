from django.core import serializers

from programming_project.forum.models import Category, Topic, Replies, User, Created


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'author', 'created')


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('name',  'author', 'created', 'content', 'tags')


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















