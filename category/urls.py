
from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    path('categories', view=views.CategoryView.as_view()),
    path('select-category', view=views.SelectCategoryView.as_view()),
    path("formcategories", view=views.CategoryFormView.as_view()),
]
