# from typing import Any
from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Category
from .forms import CategoryForm
from django.views.generic.edit import FormView,CreateView
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,DeleteView
# Create your views here.

class CreateCategoryView(CreateView):
    form_class = CategoryForm
    success_url = reverse_lazy('index')
    template_name = 'category/add_new_category.html'
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.save()
        valid = super().form_valid(form)
        return valid

class ListCategoryView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.order_by('category_name')
        return qs
    
