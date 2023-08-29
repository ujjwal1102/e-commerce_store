from typing import Any, Dict, Mapping, Optional, Type, Union
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
from .models import Category
from django import forms
class CategoryForm(ModelForm):
    
    class Meta:
        model = Category
        fields = ['category_name','parent_id']
        parent_id = forms.ChoiceField(choices=[])
        widgets = {'parent_id': forms.Select()}
        lookup_fields = {'parent_id': 'category_name'}
        
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        choices = [(value,value.category_name) for value in Category.objects.all()]
        choices.append((None,'Parent Category'))
        self.fields['parent_id'].choices = choices