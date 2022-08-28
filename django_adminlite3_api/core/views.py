
from rest_framework import viewsets, pagination, generics, filters
from rest_framework import permissions
from taggit.models import Tag

from core.models import Post
from core.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    search_fields = ['created_at']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.AllowAny]


class TagDetailView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tags=tag)


class DateDetailView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        date = self.kwargs['date']
        return Post.objects.filter(created_at=date)


class ResourceDetailView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        resource = self.kwargs['name_resource'].capitalize()
        return Post.objects.filter(resource=resource)
