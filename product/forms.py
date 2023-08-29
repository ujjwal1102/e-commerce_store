from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
# from django.forms import 
from product.models import Category
from .models import Product,ProductImages,Variant

class AddNewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','title','category','brand','cost','description','quantity','thumbnail_image']
        widgets = {'category': forms.Select()}
        category = forms.ChoiceField(choices=[])
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        choices = [(value.id,value.category_name) for value in Category.objects.all()]
        choices.append((None,'Parent Category'))
        self.fields['category'].choices = choices
      
    def save_data(self,details_json):
        name = self.cleaned_data.get('name')
        title = self.cleaned_data.get('title')
        category = self.cleaned_data.get('category')
        brand = self.cleaned_data.get('brand')
        cost = self.cleaned_data.get('cost')
        description = self.cleaned_data.get('description')
        quantity = self.cleaned_data.get('quantity')
        thumbnail_image = self.cleaned_data.get('thumbnail_image')
        details = details_json
        prod_obj = Product.objects.create(name=name,title=title,category=category,brand=brand,cost=cost,description=description,quantity=quantity,details=details_json,thumbnail_image=thumbnail_image)
        prod_obj.save()
        print(' prod_obj : ', prod_obj,prod_obj.id)
        prod_id = Product.objects.get(id=prod_obj.id)
        return prod_id


class AddProductsImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['product_images']
        widgets = {'product_images': forms.FileInput(attrs={'multiple':True})   }
    
    def save_form(self,prod_id):
        for img in self.files.getlist('product_images'):
            prod_obj = ProductImages.objects.create(product_image_id=prod_id,product_images=img)
            prod_obj.save()
        
class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ['product_id','details','cost','quantity']