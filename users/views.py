from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.edit import FormView,CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login,  update_session_auth_hash,logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User  
from .forms import Validate,SaveData,CategoryForm,ValidatRegister,ValidateProfile
from .models import Product,ProductImages,Category,Customer,Wishlist,ChildCategory,GrantChildCategory
import json
import requests
from django.db.models import Q,F
from django.views.generic.edit import CreateView,FormView

# Create your views here.
class IndexView(View):
    def get(self,request):
        prod = Product.objects.all()
        object_list = prod[:8]
        reverse_obj_list = prod.order_by("-add_on")[:4]
        user_id = User.objects.filter(id=self.request.user.id).exists()
        if user_id:
            user = User.objects.get(id=self.request.user.id)
            print(user_id,user)
            wish = Wishlist.objects.filter(user_id=user).values_list('product_id',flat=True)
            return render(request,'home.html',{'object_list':object_list,'reverse_obj_list': reverse_obj_list,'wish':wish})
        wish = []
        return render(request,'home.html',{'object_list':object_list,'reverse_obj_list': reverse_obj_list,'wish':wish})
    
class LoginView(View):
    model = User
    
    def get(self,*args, **kwargs):
        return render(self.request,'login.html')
    def post(self,*args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(self.request, username = username, password = password)
        if user is not None:
            login(self.request, user)
            messages.info(self.request, f'Successfully Logged in...')
            return redirect('index')
        else:
            messages.info(self.request, f'Please enter correct username or password')
            return self.get(self.request)

class SignUpView(View):
    model = User
    def get(self,*args, **kwargs):
        slug = self.kwargs['slug']
        print(slug)
        return render(self.request,'signup.html',{'type':slug})
    def post(self,*args, **kwargs):
        slug = self.kwargs['slug']
        print(slug)
        
        username = self.request.POST.get('username')
        email = self.request.POST.get('email')
        password1 = self.request.POST.get('password1')
        password2 = self.request.POST.get('password2')
        val = ValidatRegister()
        val_name  = val.validate_name(username)
        val_email = val.validate_email(email)
        val_passwd = val.validate_password(passwd1=password1,passwd2=password2) 
        if val_name is None:
            if val_email is None:
                if val_passwd is None:
                    user_obj = self.model()
                    user_obj.username =  username
                    user_obj.email = email
                    user_obj.password1 = password1
                    user_obj.password2 = password2
                    if slug == 'seller':
                        staff_user = True
                    else:
                        staff_user = False
                    user = self.model.objects.create_user(username=user_obj.username,email=user_obj.email,password=user_obj.password2,is_staff=staff_user)
                    user.save()
                    login(self.request, user)
                    messages.info(self.request, f'Welcome {user_obj.username},You have Successfully Registered.')
                    return redirect('index')
                else:
                    messages.info(self.request, val_passwd)
                    return redirect(self.request.path_info)
            else:
                messages.info(self.request, val_email)
                return redirect(self.request.path_info)
        else:
            messages.info(self.request, val_name)
            return redirect(self.request.path_info)
            
class LogoutView(View):
    def get(self,request):
        if self.request.user is not None:
            logout(request)
            messages.info(request, f'Successfully Logged Out')
        return redirect("index")

class CartView(View):
    def get(self,request):
        return render(request,'cart.html')
    


class ChecoutFormView(View):
    def get(self,request):
        return render(request,'check_out.html')
        
class AccountsView(View):
    def get(self, *args, **kwargs):
        context = {'type':['customer','seller']}
        return render(self.request,'accounts.html',context)
    
class ProductsListView(View):
    
    def get(self,request):
        products = Product.objects.all()
        products_images = ProductImages.objects.all()
        total = products.count()
        if self.request.user.is_authenticated:
            user_id = User.objects.get(id=self.request.user.id)
            print(user_id)
            wish = Wishlist.objects.filter(user_id=user_id).values_list('product_id',flat=True)
            print(wish)
            return render(request,'product_list.html', {'products':products,'products_images':products_images,'total':total,'wish':wish})
        return render(request,'product_list.html',{'products':products,'products_images':products_images,'total':total})

class ProductsGridView(View):
    def get(self,request,):
        products = Product.objects.all()
        products_images = ProductImages.objects.all()
        total = products.count()
        if self.request.user.is_authenticated:
            user_id = User.objects.get(id=self.request.user.id)
            print(user_id)
            wish = Wishlist.objects.filter(user_id=user_id).values_list('product_id',flat=True)
            print(wish)
            return render(request,'product_grid.html', {'products':products,'products_images':products_images,'total':total,'wish':wish})

        return render(request,'product_grid.html', {'products':products,'products_images':products_images,'total':total,})

class FeedbackView(View):
    def get(self,request):
        return render(request,'feedback.html')
class ShopByCategoryView(View):
    def get(self, *args, **kwargs):
        id = self.kwargs['id']
        object_list = Product.objects.filter(category=id)
        print(object_list)
        category = Category.objects.filter(category_uid=id)
        child_cat = ChildCategory.objects.filter(Q(category_uid = id))
        print("child_cat : ",child_cat)
        print(category)  
        return render(self.request,'search_results.html',{'category':category,'object_list':object_list,'child_cat':child_cat})

class FilterVew(TemplateView):
    template_name = "search_result_card.html"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        brand = self.request.GET.getlist('brand')
        print(brand)
        context["object_list"] = Product.objects.filter(Q(brand__in=brand) | Q(brand__exact=brand))
        return context
    
class FilterView(View):
    def get(self, *args, **kwargs):
        brand = self.request.GET.get('brand')
        price = self.request.GET.get('price')
        brand = json.loads(brand)
        price = json.loads(price)
        price = int(price[0])
        print("brand : ",brand,'price : ',price)
        sp = str(self.request.META['HTTP_REFERER'])
        if ('?q' in sp):
            if (len(brand) == 0) | (brand == None):
                print('===============================')
                
                query= str(sp.split('?')[1]).split("=")[1]
                print(query)
                object_list = Product.objects.filter(cost__lt=price)
                print(object_list)
                print("brend ----",brand)

                return render(self.request,'search_result_card.html',{'object_list':object_list})
            else :    
                print('else'    )
                object_list = Product.objects.filter(Q(brand__in=brand) & Q(cost__lt=price))
        if ('categories' in sp):
            print('categories')
            if (len(brand) == 0) | (brand == None):
                query = sp.split('/')[-1]
                print(query)
                object_list = Product.objects.filter(Q(category=query)  & Q(cost__lt=price) )
                return render(self.request,'search_result_card.html',{'object_list':object_list})
            else:                
                object_list = Product.objects.filter(Q(brand__in=brand) & Q(cost__lt=price))
        print('last')
        return render(self.request,'search_result_card.html',{'object_list':object_list})
       
class CategoriesListView(View):
    def get(self, *args, **kwargs):
        prod_cat = Category.objects.all()
        return render(self.request,'categories_list.html',{'prod_cat':prod_cat,})
    
def add_to_cart(request):
    quan = request.POST.get('quantity')
    id = request.POST.get('id')
    obj = Product.objects.get(product_id=id)
    print(obj.product_id)
    print(request.session['cart'])
    cart = request.session.get('cart',{})
    cart[id] = cart.get(id, quan)
    print(request.session['cart']) 
    
class ProductDetailView(View):
    
    def get(self, *args, **kwargs):
        id = self.kwargs['id']
        product = Product.objects.get(product_id = id)
        print('get')
        product_images = ProductImages.objects.filter(product_image_id=product)     
        product_detail = product.details
        product_cost = product.cost
        product_desc = product.description
        print(type(eval(product_detail))) 
        return render(self.request,'product_detail.html',{'product_id':id,'product_desc':product_desc,'product_cost':product_cost,'product':product,'product_images':product_images,'product_detail' : eval(product_detail)})
    
    def post(self, *args, **kwargs):
        quan = self.request.POST.get('quantity')
        id = self.request.POST.get('id')
        obj = Product.objects.get(product_id=id)
        print(obj.product_id)
        cart = self.request.session.get('cart',{})
        cart[id] = cart.get(id, quan)
        self.request.session['cart'] = cart
        print(self.request.session['cart'])
        return redirect('cart')
            
class dynamicform(View):
    def get(self, *args, **kwargs):
        return render(self.request,'dynamic_row_add.html')
    def post(self, *args, **kwargs):
        name = self.request.POST.get('name')
        mname = self.request.POST.get('mydata')
        mydata = json.loads(mname)
        print(name,mydata)
        for data in mydata['formdata']:
            c = data.split(':')
            print(c)
        return render(self.request,'dynamic_row_add.html')
    
class AddProductView(View):
    def get(self, *args, **kwargs):
        c_dict = {}
        
        
        cat = Category.objects.all()
        for c in cat:
            print('|---> category_name : ',c.category_name)
            cc = ChildCategory.objects.filter(category_uid = c)
            c_c_dict = {}
            for gc in cc:
                print('|------> child_category_name :',gc.child_category_name)
                gcc = GrantChildCategory.objects.filter(child_category_id=gc)
                g_c_c_list = []
                for i in gcc:
                    print('|----------> grant_child_category_name : ',i.grant_child_category_name)
                    g_c_c_list.append(i.grant_child_category_name)
                c_c_dict[gc.child_category_name] = g_c_c_list
            c_dict[c.category_name] = c_c_dict
        print(c_dict)
        cat_list = Category.objects.all().values_list('category_name',flat=True)
        child_cat = ChildCategory.objects.all().values_list('child_category_name',flat=True)
        grant_child_cat = GrantChildCategory.objects.all().values_list('grant_child_category_name',flat=True)
        return render(self.request,'add_a_new_product.html',{'cat_list':cat_list,'child_cat':child_cat,'grant_child_cat':grant_child_cat,'c_dict':c_dict})
    
    def post(self, *args, **kwargs):
        print(self.request.POST['category'])
        print(self.request.FILES['images'])
        data = Validate().adding_product(self.request,self.request.POST,self.request.FILES.getlist('images'))
        print(data)
        done = SaveData().save(data)
        print(done)
        messages.success(self.request,done)
        return render(self.request,'add_a_new_product.html')
        
def faltu(request):
    
    
    import requests

    url = "https://moviesdatabase.p.rapidapi.com/titles/x/titles-by-ids"

    querystring = {"idsList":"tt0001702,tt0001856,tt0001856"}

    headers = {
    	"X-RapidAPI-Key": "037786a6f3mshff43f34999525bdp17b954jsn32eccfa4f696",
    	"X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(str(json.loads(response) ) )
    return render(request,"faltu.html",{'data':response})


#=======================================================================#

class WishlistView(View):
    def get(self, *args, **kwargs):
        try:
            products = Wishlist.objects.filter(user_id = self.request.user.id).values_list('product_id')
            wishlist = Product.objects.filter(product_id__in=products)
            print(wishlist)
            return render(self.request,'wishlist.html',{'products':wishlist})
        except Wishlist.DoesNotExist:
            products = 0
            print(products)
            return render(self.request,'wishlist.html',{'products':products})
    def post(self, *args, **kwargs):
        
            user = self.request.user.id
            prod = self.request.POST.get('product_id')
            user = User.objects.filter(id=self.request.user.id).exists()
            if user:
                user = User.objects.get(id=self.request.user.id)
                prod = Product.objects.get(product_id=prod)
                print(user,prod)
                # try:
                if not (Wishlist.objects.filter(user_id=user,product_id=prod).exists()):
                    wishitem = Wishlist.objects.create(user_id=user,product_id=prod)
                    wishitem.save()
                    messages.error(self.request,'Item Added to Wishlist')
                    return redirect(self.request.META.get('HTTP_REFERER'))
                else:
                    wishitem = Wishlist.objects.get(user_id=user,product_id=prod)
                    wishitem.delete()
                    messages.error(self.request,'Item Deleted from Wishlist')
                    return redirect(self.request.META.get('HTTP_REFERER'))
            else :
                messages.error(self.request,'Sorry, You are Not Authenticated')
                return redirect(self.request.META.get('HTTP_REFERER'))
        
        
class RemoveFromWishlist(View):
    def post(self, *args, **kwargs):
        user = self.request.user.id
        prod = self.request.POST.get('product_id')
        user = User.objects.get(id=self.request.user.id)
        prod = Product.objects.get(product_id=prod)
        print(user,prod)
        wishitem = Wishlist.objects.filter(product_id=prod,user_id=user)
        print('--------------------------item deleted',wishitem)
        wishitem.delete()
        
        return redirect(self.request.META.get('HTTP_REFERER'))
#--------------------# CART #----------------------#

class CartView(View):
    def get(self, *args, **kwargs):
        user_id = User.objects.get(id=self.request.user.id)
        print(user_id)
        wish = Wishlist.objects.filter(user_id=user_id).values_list('product_id',flat=True)
        products = []
        no_of_products = None
        
        if 'cart' in self.request.session.keys() :
            print(type(self.request.session['cart']))
            for s,p in self.request.session['cart'].items():
                print(s,p)
                products.append((Product.objects.get(product_id=s),p))
            no_of_products = products.count
            print(products)
        else:
            print('cart empty')
        return render(self.request,'cart.html',{'products':products,'no_of_products':no_of_products,'wish':wish})

class AddToCart(View):
    def get(self, *args, **kwargs):
        quan = self.request.POST.get('quantity')
        id = self.request.POST.get('id')
        obj = Product.objects.get(product_id=id)
        print(obj.product_id)
        cart = self.request.session.get('cart',{})
        cart[id] = cart.get(id, quan)
        self.request.session['cart'] = cart
        print(self.request.session['cart']) 
        return redirect(self.request.META.get('HTTP_REFERER'))
    def post(self, *args, **kwargs):
        quan = self.request.POST.get('quantity')
        id = self.request.POST.get('id')
        obj = Product.objects.get(product_id=id)
        print(obj.product_id)
        cart = self.request.session.get('cart',{})
        cart[id] = cart.get(id, quan)
        self.request.session['cart'] = cart
        print(self.request.session['cart']) 
        return redirect(self.request.META.get('HTTP_REFERER'))
    

class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        try:
            id = self.kwargs['id']
            print('===================================')
            print(id)
            print("request.session['cart'][id]", self.request.session['cart'][id])
            print('Before',self.request.session['cart'])
            del self.request.session['cart'][id]
            print('After',self.request.session['cart'])
            self.request.session.modified = True
            print('session deleted')
        except KeyError:
            pass
        return redirect('cart')


#======================================================================================
states = ["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry"]
country = ['India']
class ProfileView(View):
    def get(self, *args, **kwargs):
        try:
            obj = Customer.objects.get(user=self.request.user.id)
        except Customer.DoesNotExist:
            return render(self.request,'profile_not_exist.html')
        return render(self.request,'profile.html',{'obj':obj})
    
class CreateProfileView(View):
    def get(self, *args, **kwargs):
        
        return render(self.request,'profile_create.html',{'states':states,'country':country})
    def post(self, *args, **kwargs):
        firstname = self.request.POST['firstname']
        lastname = self.request.POST['lastname']
        phone = self.request.POST['phone']
        state = self.request.POST['state']
        country = self.request.POST['country']
        address = self.request.POST['address']
        pf_dict = {'firstname':firstname,'lastname':lastname,'phone':phone,'state':state,'country':country,'address':address}
        valid_profile = ValidateProfile()
        err_msg = valid_profile.checkprofile(pf_dict=pf_dict)
        if err_msg is None:
            print(pf_dict)
            msg = valid_profile.save(pf_dict=pf_dict,user=self.request.user.id)
            if msg is not None:
                messages.success(self.request,msg)
                return redirect('profile')
            return redirect('create_profile')
        else:
            print(err_msg)
            messages.error(self.request,err_msg)
            return redirect('create_profile')
class UpdateProfileView(View):
    def get(self, *args, **kwargs):
        obj = Customer.objects.get(user=self.request.user.id)
        
        return render(self.request,'profile_update.html', {'states':states,'country':country,'obj':obj})

    def post(self, *args, **kwargs):
        firstname = self.request.POST['firstname']
        lastname = self.request.POST['lastname']
        phone = self.request.POST['phone']
        state = self.request.POST['state']
        country = self.request.POST['country']
        address = self.request.POST['address']
        pf_dict = {'firstname':firstname,'lastname':lastname,'phone':phone,'state':state,'country':country,'address':address}
        valid_profile = ValidateProfile()
        err_msg = valid_profile.checkprofile(pf_dict=pf_dict)
        if err_msg is None:
            print(pf_dict)
            msg = valid_profile.saveupdatedprofile(pf_dict=pf_dict,user=self.request.user.id)
            if msg is not None:
                messages.success(self.request,msg)
                return redirect('profile')
            return redirect('update_profile')
        else:
            print(err_msg)
            messages.error(self.request,err_msg)
            return redirect('update_profile')

#======================================================================
class CategoryView(View):
    
    def get(self, *args, **kwargs):
        return render(self.request,'categories.html')

class AddCategoryView(View):
    def get(self,*args, **kwargs):
        return render(self.request,'add_categories.html', )

    def post(self,*args, **kwargs):
        category_name = self.request.POST['category']
        val = CategoryForm().validate(category_name)
        print(val)
        
        if val.keys():
            if 'error' in val.keys():
                print(val['error'])
                messages.error(self.request,val['error'])
                return redirect('add_category')
            else :
                print(val['success'])
                messages.success(self.request,val['success'])
                return redirect('index')
       
    
class AddChildCategoryView(View):
    cat_list = Category.objects.all().values_list('category_name',flat=True)
    
    def get(self, *args, **kwargs):
        return render(self.request,'add_child_category.html',{'cat_list':self.cat_list})
    def post(self, *args, **kwargs):
        cat_name = self.request.POST['cat_name']
        child_cat_name = self.request.POST['child_category']
        cat_id = Category.objects.get(category_name=str(cat_name))
        
        child_cat_obj = ChildCategory.objects.create(category_uid = cat_id,child_category_name = child_cat_name)
        child_cat_obj.save()
        messages.success(self.request,'Child Category Added Successfully')
        print(cat_id.category_uid ,cat_name,child_cat_name)
        return render(self.request,'add_child_category.html',{'cat_list':self.cat_list})

    
class AddGrantChildCategoryView(View):
    cat_list = Category.objects.all().values_list('category_uid','category_name')
    cat_dict = {}
    
    def get(self, *args, **kwargs):
        for cat in self.cat_list:
            child_cat = ChildCategory.objects.filter(category_uid=cat[0])
            if child_cat.exists():
                sub_cat_list = list()
                for categories in child_cat:
                    name = categories.child_category_name
                    sub_cat_list.append(str(name))        
                self.cat_dict[str(cat[1])] = sub_cat_list  
            else:
                self.cat_dict[cat[1]] = []
        return render(self.request,'add_grant_child_category.html' ,{'cat_dict':self.cat_dict})
    
    
    def post(self, *args, **kwargs):
        category = self.request.POST['category']
        child_category = self.request.POST['child_category']
        grant_child_category = self.request.POST['grant_child_category']
        print(category,child_category,grant_child_category)
        child_cat_id = ChildCategory.objects.get(child_category_name = child_category)
        grant_child_cat_obj = GrantChildCategory.objects.create(child_category_id=child_cat_id,grant_child_category_name = grant_child_category)
        grant_child_cat_obj.save()
        messages.success(self.request,'Grant Child Category Added Successfully.....!!!!')
        return self.get()
    
class SearchView(ListView):
    model = Product
    template_name = "search_results.html"
    def get_queryset(self) :
        self.query = self.request.GET.get('q')
        print(self.query)
        self.object_list = Product.objects.filter(
            Q(name__contains=self.query) | Q(title__icontains=self.query) 
        )
        print(self.object_list)
        return self.object_list
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        cat = self.object_list.values_list('category').distinct()
        print(self.object_list.values_list('category',flat=True).distinct())
        context['category'] = Category.objects.filter(category_uid__in=cat)
        print(context['category'])
        return context
    
    