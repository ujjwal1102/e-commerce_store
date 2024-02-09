# # from typing import Any, Dict, Mapping, Optional, Type, Union
# # from django.core.files.base import File
# # from django.db.models.base import Model
# from django.forms import ModelForm
# # from django.forms.utils import ErrorList
# from django.shortcuts import get_object_or_404
# from .models import Category
# from django import forms
# class CategoryForm(ModelForm):
    
#     class Meta:
#         model = Category
#         fields = ['category_name','parent_id']
#         parent_id = forms.ChoiceField(choices=[])
#         widgets = {'parent_id': forms.Select()}
#         lookup_fields = {'parent_id': 'category_name'}
        
#     def __init__(self,*args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)
#         choices = [(value,value.category_name) for value in Category.objects.all()]
#         choices.append((None,'Parent Category'))
#         self.fields['parent_id'].choices = choices
        
        
# class AddCategoryForm():
#     def __init__(self) -> None:
#         pass
#     def can_create_data(self,name):
        
#         original_name = name
#         firstcap_name = name.capitalize()
#         allcaps_name= name.upper()
#         alllower_name = name.lower()
        
        
#         if Category.objects.filter(category_name= (original_name or firstcap_name or allcaps_name or alllower_name) ).exists():
#             return False
        
#         else:
#             return True
            
        
#     def save(self,name,id):
#         name = name.capitalize()
#         parent_id = get_object_or_404(Category,id=id)
#         cat = Category.objects.create(category_name=name,parent_id=parent_id)
#         cat.save()
        
#         return cat
        
        
        
    
    