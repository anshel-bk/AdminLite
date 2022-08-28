from rest_framework import serializers
from taggit.models import Tag
from taggit.serializers import TaggitSerializer

from .models import Post


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("title", "resource", "created_at", "tags")
