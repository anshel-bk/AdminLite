from django.urls import include, path

from adminlte3.views import home_page


urlpatterns = [
    path('', home_page, name='index'),
]
