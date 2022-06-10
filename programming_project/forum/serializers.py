from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from .models import Category, Topic, Replies, User, Created, Feedback
from .services import BlogService


class TopicUnSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')

    class Meta:
        model = Topic
        fields = (
            'id', 'name', 'url', 'author', 'category',
            'created', 'content', 'tags', 'category'
        )


class CategorySerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Category
    #     fields = ('name', 'author', 'created', 'url', 'topic')

    slug = serializers.SlugField(read_only=True, allow_unicode=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'author', 'topic')


class TopicSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    category = CategorySerializer

    class Meta:
        model = Topic
        fields = ('name', 'url', 'category','content', 'author', 'created')


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


class TopicListSerializers(serializers.ModelSerializer):
    category = CategorySerializer()
    profit = serializers.SerializerMethodField(method_name='get_profit')

    def get_profit(self, obj):
        return obj.fess_in_world - obj.budget

    class Meta:
        model = Topic
        fields = ('id', 'name', 'category', 'profit')


class TopicDetailSerializer(serializers.ModelSerializer):
    """Полный фильм"""
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Topic


class CreateTopicSerializer(TaggitSerializer, serializers.ModelSerializer):
    objects = None
    tags = TagListSerializerField()

    class Meta:
        model = Topic
        fields = ('name', 'category', 'image', 'content', 'tags')

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return super().create(validated_data)

    def validate_title(self, name: str):
        if BlogService.is_article_slug_exist(name):
            raise serializers.ValidationError("This title already exists")
        return name



class FeedbackSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    name = serializers.CharField(min_length=2, required=False)

    class Meta:
        model = Feedback
        fields = ('name', 'email', 'content', 'file')

    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['name'] = user.full_name()
            validated_data['email'] = user.email
        return super().create(validated_data)





