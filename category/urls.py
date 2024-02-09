
from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    path('categories', view=views.CategoryView.as_view())
]
