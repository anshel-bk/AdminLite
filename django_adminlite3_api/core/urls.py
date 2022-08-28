from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import PostViewSet, TagDetailView, DateDetailView, ResourceDetailView

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path("tags/<slug:tag_slug>/", TagDetailView.as_view()),
    path("date/<str:date>/", DateDetailView.as_view()),
    path("resource/<name_resource>/", ResourceDetailView.as_view())
]
