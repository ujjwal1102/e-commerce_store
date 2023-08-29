from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from .models import Product,ProductImages
# Create your views here.
import json
from .forms import AddNewProductForm,AddProductsImagesForm,VariantForm
from django.views.generic.edit import CreateView,FormView
from django.views.generic import ListView,DetailView

class AddProductView(FormView):
    form_class = [AddNewProductForm,AddProductsImagesForm]
    template_name = 'products/add_products_form.html'
    
    def get(self, request):
        form1 = AddNewProductForm()
        form2 = AddProductsImagesForm()
        print(form1.fields['category'].choices)
        return render(self.request, 'products/add_product_form.html', {'form1': form1, 'form2': form2})
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) :
        # context = super().post(request, *args, **kwargs)
        form1 = AddNewProductForm(self.request.POST,self.request.FILES)
        form2 = AddProductsImagesForm(self.request.POST,self.request.FILES)
        if form1.is_valid() and form2.is_valid():
            print('CORRECT')

            featurename = self.request.POST.getlist('featurename')
            featurevalue = self.request.POST.getlist('featurevalue')
            print(featurename,len(featurename),featurevalue,len(featurevalue))
            details_dict = {}
            for i in range(len(featurename)):
                details_dict[featurename[i]] = featurevalue[i]
            print(details_dict)
            details_json = json.dumps(details_dict)
            prod_id = form1.save_data(details_json=details_json)
            form2.save_form(prod_id=prod_id)
          
            print("Form Saved Successfully")
                    
            return redirect('index')
        else:            
            print('form1.errors : ',form1.errors)
            print('form2.errors : ',form2.errors)
            return render(request, 'products/add_product_form.html', {'form1':form1,'form2':form2})

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_images'] = ProductImages.objects.filter(product_image_id =  self.kwargs['pk'])
        context['details'] = json.loads(context['object'].details)
        print(type(context['details']))
        return context