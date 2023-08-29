from django import forms
from .models import Product,Customer,ProductImages,Category,ChildCategory,GrantChildCategory
import re,json
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
class SaveData:
    def save(self,my_data):
        prod_obj = Product()
        prod_obj.product_id = my_data['product_id']
        prod_obj.category = my_data['category']
        prod_obj.child_category = my_data['childcategory']
        prod_obj.grant_child_category = my_data['grantchildcategory']
        prod_obj.brand = my_data['brand']
        prod_obj.name = my_data['name']
        prod_obj.title = my_data['title']
        prod_obj.details = my_data['details']
        prod_obj.cost = my_data['cost']
        prod_obj.description = my_data['description']
        prod_obj.product_images = my_data['images'][0]
        prod_obj.save()
        print('Product Succesfully saved')
        obj = Product.objects.get(product_id = my_data['product_id'])
        print(obj)
        
        
        for img in range(1,len(my_data['images'])):
            prod_image_obj = ProductImages.objects.create(
                product_image_id=obj,
                product_images = my_data['images'][img]
            )
            prod_image_obj.save()
        print('Succesfully saved with Images')
        return 'product Saved Successfully'
def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
class Validate:
    model = Product
    
    def p_uid(self,category):
        
        last_product_id = self.model.objects.all().order_by('-add_on').values('product_id')
        if not last_product_id:
            return 'P'+'-'+str(1).zfill(4)
        p_id = last_product_id.first()['product_id']
        p_last_digit = p_id[-4:]
        new_p_last_digit = int(p_last_digit)+1
        new_p_id = 'P' + '-' + str(new_p_last_digit).zfill(4)
        
        return new_p_id

    # def cell_phone_accessories(self,request,category):
        
    #     name = request.POST.get('name')
    #     title = request.POST.get('title')
    #     brand = request.POST.get('brand')
    #     color = request.POST.get('color')
    #     price = request.POST.get('price')
    #     ram = request.POST.get('ram')
    #     battery = request.POST.get('battery')
    #     camera = request.POST.get('camera')
    #     display = request.POST.get('display')
    #     memory = request.POST.get('memory')
    #     quantity = request.POST.get('quantity')
    #     description = request.POST.get('description')
    #     images = request.FILES.getlist('images')
    
    #     p_id = self.p_uid(category=category)
    #     detail_items = [name,title,brand,color,ram,battery,camera,display,memory]
    #     data='-'
    #     data = data.join(detail_items)
    #     print(data)
    #     m_dict = {'product_id':p_id,'category':category,'cost':price,'details':data,'description':description,'quantity':quantity,'images':images}
    #     return m_dict
    
    # def music_accessories(self,request,category):
    #     name = request.POST.get('m_name')
    #     cost = request.POST.get('m_cost')
    #     material = request.POST.get('m_material')
    #     color = request.POST.get('m_color')
    #     type = request.POST.get('m_type')
    #     quantity = request.POST.get('m_quantity')
    #     description = request.POST.get('description')
    #     images = request.FILES.getlist('m_images')
    #     p_id = self.p_uid(category=category)
    #     detail_items = [name,material,color,type]
    #     data='-'
    #     data = data.join(detail_items)
    #     print(data)
    #     m_dict = {'product_id':p_id,'category':category,'cost':cost,'details':data,'description':description,'quantity':quantity,'images':images}
    #     return m_dict
    
    # def register_new_product(self,request,mydata):
    #     images = request.FILES.getlist('images')
    #     print(images)
    #     dict = {}
    #     for data in mydata['features']:
    #         c = data.split(':')
    #         dict[c[0]] = c[1]
    #     # print(dict)
    #     features = {}
    #     features_key = []
    #     features_value = []
    #     for key,value in dict.items():
    #         if 'feature_name' in key:
    #             features_key.append(value)  
    #     for key,value in dict.items():   
    #         if 'feature_value' in key:
    #             features_value.append(value)
    #     if len(features_key) == len(features_value):
    #         # print('yes')
    #         for f in range(len(features_key)):
    #             features[features_key[f]] = features_value[f]
        
    #     p_id = self.p_uid(category=dict['category'])
    #     category = dict['category']
        
    #     price = dict['product_price']
    #     description = dict['description']
    #     quantity = dict['product_quantity']
    #     details = json.dumps(features)
    #     print(json.loads(details))
    #     m_dict = {'product_id':p_id,'category':category,'cost':price,'details':details,'description':description,'quantity':quantity,'images':images}
    #     print(m_dict)
    
    def adding_product(self,request,data,imgs):
        p_id = self.p_uid(category=data['category'])
        
        name = data['product_name']
        title = data['product_title']
        category = Category.objects.get(category_name=data['category']) 
        print(category)
        child_category = ChildCategory.objects.get(child_category_name=data['childcategory'])
        print(child_category)
        print(GrantChildCategory.objects.get(grant_child_category_name = str(data['grantchildcategory'])))
        grant_child_category = GrantChildCategory.objects.get(grant_child_category_name = data['grantchildcategory'])
        print(grant_child_category)
        price = data['product_price']
        brand = data['product_brand']
        features = {}
        # features_key = []
        # features_value = []
        if data['feature_name1']:
            f = 1
            while data[f'feature_name{f}']:
                features[data[f'feature_name{f}']] = data[f'feature_value{f}']
                if f'feature_name{f+1}' in data:
                    f=f+1
                    pass
                else:
                    break
        details = features
        description = str(data['description'])
        quantity = data['product_quantity']
        images=imgs
        m_dict = {'product_id':p_id,
                  'name':name,
                  'title':title,
                  'brand':brand,
                  'category':category,
                  'childcategory':child_category,
                  'grantchildcategory':grant_child_category,
                  'cost':price,
                  'details':details,
                  'description':description,
                  'quantity':quantity,
                  'images':images}
        return m_dict
    
class CategoryForm():
    model = Category
    
    def cat_uid(self,category):
        # print(self.model.objects.all().order_by('-category_uid').values('category_uid'))
        last_category_uid = self.model.objects.all().order_by('-category_uid').values('category_uid')
        print(last_category_uid)
        if not last_category_uid:
            
            return 'CAT'+'-'+str(1).zfill(4)
        c_uid = last_category_uid.first()['category_uid']
        c_last_digit = c_uid[-4:]
        new_c_last_digit = int(c_last_digit)+1
        new_c_uid = 'CAT' + '-' + str(new_c_last_digit).zfill(4)
        return new_c_uid
    def validate(self,category_name):
        my_dict = {}
        if category_name is not None:
            if category_name == '':
                error = 'Please enter the Name Of Category'
                my_dict['error'] = error
                return my_dict
            
            if len(category_name) <= 4:
                error = 'Name Of Category Must be greater than 4 Characters'
                my_dict['error'] = error
                return my_dict
            if category_name.isnumeric():
                print(category_name)
                error = 'Category Name cannot contains numbers'
                my_dict['error'] = error
                return my_dict
            
            obj = Category()
            try:
                obj.category_name = category_name
                print(category_name)
                print(self.cat_uid(category_name))
                obj.category_uid = self.cat_uid(category_name)
                print(obj.category_uid)
                try :
                    print('inside try')
                    print(f'{obj.category_name},{obj.category_uid}')
                    obj.save()
                    my_dict['success'] = f'{obj.category_name} Category is Successfully Added'
                    return my_dict
                except:
                    my_dict['success'] = f'{obj.category_name} Isn\'t Created'
                    return my_dict
            except:
                return f'Category Not Added'

class ValidatRegister():
    model = User
    error_msg = None
    def validate_name(self,name):
        if name is not None:
            if len(name)<4:
                self.error_msg = 'Username length must be greater than 4'
            if name in self.model.objects.all().values_list('username',flat=True):
                self.error_msg = 'Username Already Exist, Choose Another Username'
            return self.error_msg
        else:
            self.error_msg= 'Please Enter Username'
            return self.error_msg 
            
    def validate_email(self,email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if email is not None:
            if email in self.model.objects.all().values_list('email',flat=True):
                self.error_msg = 'Email exist'
            if not (re.fullmatch(regex, email)):
                self.error_msg = 'Please Enter Valid Email'
            return self.error_msg    
        else:
            self.error_msg = 'Please Enter Email'
            return self.error_msg
        
    def validate_password(self,passwd1,passwd2):
        if (passwd1 or passwd2) is not None:
            if len(passwd1)<8:
                self.error_msg = 'This password is too short. It must contain at least 8 characters.' 
            if passwd1 != passwd2:
                self.error_msg = 'Password Mismatch'
            return self.error_msg
        else:
            self.error_msg = 'Please Enter Password'
            return self.error_msg
            
            
class ValidateProfile():
    def checkprofile(self,pf_dict):
        error_msg=None
        print(type(pf_dict['phone']))
        if len(pf_dict['firstname'])<4:
            error_msg = 'Firstname must contains at least 4 letters'
        if pf_dict['firstname'].isalpha == False:
            error_msg = 'Firstname must contains only letters'
        if len(pf_dict['lastname'])<4:
            error_msg = 'Lastname  must contains at least 4 letters '
        if pf_dict['lastname'].isalpha == False:
            error_msg = 'Lastname must contains only letters'
        if not pf_dict['state']:
            error_msg = 'Please Select State'
        if not pf_dict['country']:
            error_msg = 'Please Select State'
        if (not (len(pf_dict['phone'])==10) ) or (not (pf_dict['phone'].isnumeric())):
            
            error_msg = 'Please enter correct Phone No (must be 10 digits)'
        if not pf_dict['address']:
            error_msg = 'Please Enter Address'
        return error_msg  
    def save(self,pf_dict,user):
        userid = User.objects.get(id=user)
        msg = None
        model = Customer()
        model.user = userid
        model.first_name = pf_dict['firstname']
        model.last_name = pf_dict['lastname']
        model.phone = pf_dict['phone']
        model.country = pf_dict['country']
        model.state = pf_dict['state']
        model.address = pf_dict['address']
        model.save()
        msg = 'Profile Created Successfully'
        return msg
    
    def saveupdatedprofile(self,pf_dict,user):
        update_profile = Customer.objects.get(user=user)
        update_profile.first_name = pf_dict['firstname']
        update_profile.last_name = pf_dict['lastname']
        update_profile.phone = pf_dict['phone']
        update_profile.country = pf_dict['country']
        update_profile.state = pf_dict['state']
        update_profile.address = pf_dict['address']
        update_profile.save()
        msg = 'Profile Updated Successfully'
        return msg
    
class AddCategoryForm(forms.Form):
    category = forms.CharField(max_length=150,widget=forms.TextInput(attrs={"required": True,"class":"form-control" ,"name":"category", "placeholder":"Enter Category Name"}))
    
    
# class ChildCategoryForm(forms.Form):
#     category = forms.ChoiceField(choices=Category.objects.all().values_list('category_name',flat=True),widget=forms.Select(attrs={"required": True,"class":"form-control" ,"name":"category", "placeholder":"Enter Category Name"}))
#     # category = forms.CharField(max_length=150,widget=forms.TextInput(attrs={"required": True,"class":"form-control" ,"name":"category", "placeholder":"Enter Category Name"}))
#     child_category = forms.CharField(max_length=150,widget=forms.TextInput(attrs={"required": True,"class":"form-control" ,"name":"category", "placeholder":"Enter Category Name"}))
    
    
# class GrantChildCategoryForm(forms.Form):
#     pass