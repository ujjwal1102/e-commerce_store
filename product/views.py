# from typing import Any, Dict
# from django.http import HttpRequest, HttpResponse
# from django.shortcuts import render,redirect
# from .models import Product,ProductImages
# # Create your views here.
# import json
# from .forms import AddNewProductForm,AddProductsImagesForm,VariantForm
# from django.views.generic.edit import CreateView,FormView
# from django.views.generic import ListView,DetailView
# from django.views import View


# class AddProductView(FormView):
#     form_class = [AddNewProductForm,AddProductsImagesForm]
#     template_name = 'products/add_products_form.html'

#     def get(self, request):
#         form1 = AddNewProductForm()
#         form2 = AddProductsImagesForm()
#         print(form1.fields['category'].choices)
#         return render(self.request, 'products/add_product_form.html', {'form1': form1, 'form2': form2})

#     def post(self, request: HttpRequest, *args: str, **kwargs: Any) :
#         # context = super().post(request, *args, **kwargs)
#         form1 = AddNewProductForm(self.request.POST,self.request.FILES)
#         form2 = AddProductsImagesForm(self.request.POST,self.request.FILES)
#         if form1.is_valid() and form2.is_valid():
#             print('CORRECT')

#             featurename = self.request.POST.getlist('featurename')
#             featurevalue = self.request.POST.getlist('featurevalue')
#             print(featurename,len(featurename),featurevalue,len(featurevalue))
#             details_dict = {}
#             for i in range(len(featurename)):
#                 details_dict[featurename[i]] = featurevalue[i]
#             print(details_dict)
#             details_json = json.dumps(details_dict)
#             prod_id = form1.save_data(details_json=details_json)
#             form2.save_form(prod_id=prod_id)

#             print("Form Saved Successfully")

#             return redirect('index')
#         else:
#             print('form1.errors : ',form1.errors)
#             print('form2.errors : ',form2.errors)
#             return render(request, 'products/add_product_form.html', {'form1':form1,'form2':form2})

# class ProductListView(ListView):
#     model = Product
#     template_name = 'products/product_list.html'

# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'products/product_detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['product_images'] = ProductImages.objects.filter(product_image_id =  self.kwargs['pk'])
#         context['details'] = json.loads(context['object'].details)
#         print(type(context['details']))
#         return context

# class Seller(View):
#     def get(self,*args,**kwargs):
#         return render(self.request,'seller/homepage.html')

# class AddMyProd(View):
#     def get(self,*args,**kwargs):
#         return render(self.request,'seller/catalog/add_product.html')
from typing import Any
from rest_framework.views import APIView
from .serializers import ProductSerializer, BrandSerializer
from rest_framework.response import Response
from product.models import Product, Brand
from category.models import Category
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
# from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView
from wishlist.models import ProductWishlist
from wishlist.serializers import WishlistSerializer
from rest_framework.decorators import api_view
import json

from rest_framework.pagination import PageNumberPagination
from django.conf import settings

from rest_framework.pagination import LimitOffsetPagination


from django.db.models import Window, F, Count, Q, Max, Min, Case, CharField, When, Value
from django.db.models.functions import Substr


class MyCustomPagination(PageNumberPagination):
    page_size = 9

    # def get_paginated_response(self, data):
    #     return Response({
    #         "page":self.get_page_number(),
    #         "next":self.page.next_page_number,
    #         "previous":self.page.previous_page_number(),
    #         "count":self.page.paginator.count(),
    #         "results":data,
    #     })


def dynamic_attributes_filtering_products(self, products, keysdict):
    print(1)

    filters = Q()  # Initialize an empty Q object for filtering

    dynamic_filters = {
        "brands": "brand__id__in",
        "categories": "category__id__in",
        "price_range": lambda value: Q(cost__gte=value['min'], cost__lte=value['max']),
        "brand": "brand__id__in",
        # Add more dynamic filters as needed
    }

    for key, value in keysdict.items():
        if key in dynamic_filters and value:
            if callable(dynamic_filters[key]):
                # If the filter is a function, call it with the value
                filters &= dynamic_filters[key](value)
            else:
                # Otherwise, apply the filter directly
                filters &= Q(**{dynamic_filters[key]: value})

    # Apply the dynamic filters to the queryset
    products = products.filter(filters)

    return products.order_by("id")


class ProductsAPIView(APIView):

    def get(self, request, format=None):
        try:
            products = Product.objects.all()[:8:1]
            wishlist_items = None
            if request.user.is_authenticated:
                wishlist_items = ProductWishlist.objects.filter(
                    user=request.user, product__in=products)
            else:
                wishlist_items = ProductWishlist.objects.none()
            print("wishlist_items", wishlist_items)
            serialized_products = ProductSerializer(products, many=True).data
            wishlist_serializer = WishlistSerializer(
                wishlist_items, many=True).data
            wl_item = [ws['product']['id'] for ws in wishlist_serializer]

            return Response(data={"data": serialized_products, "wl_item": wl_item}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={"exception": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):


        print("request.data", request.data, "request.data.json.loads",
              json.loads(request.data['features']))
        serializer = ProductSerializer(data=request.data)
        try:
            print(serializer)
            if serializer.is_valid():
                print(serializer)
                product = "Saved"
                product = serializer.save()
                print(True, 'Valid', serializer)
                return Response(data="Product added Successfully", status=status.HTTP_201_CREATED)
            else:
                print("serializer.error_messages : ", serializer.error_messages,
                      "\nserializer.errors : ", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('Exception : ', e)
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # custom_serializer = {"id":serializer.data["id"],"thumbnail_image": serializer.data["thumbnail_image"],"cost":serializer.data["cost"],"title":serializer.data["title"],"description":serializer.data["description"],"features":serializer.data["features"],"image_url":serializer.data["image_url"],"quantity":serializer.data["quantity"],"discount_price":serializer.data["discount_price"],"created_at":serializer.data["created_at",]}
        serialized_data = serializer.data
        return Response(serialized_data)


class SellerProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_id = self.request.user.id
            paginator = MyCustomPagination()
            products = Product.objects.filter(seller__id=user_id)
            paginated_products = paginator.paginate_queryset(
                products, self.request)
            serializer = ProductSerializer(
                paginated_products, many=True).data
            return Response(data={"products": serializer, "total_count": products.count(),
                                  "page": {"total_page": paginator.page.paginator.num_pages,
                                           "current_page": paginator.page.number,
                                           'next_page_number': paginator.page.next_page_number() if paginator.page.has_next() else None,
                                           'previous_page_number': paginator.page.previous_page_number() if paginator.page.has_previous() else None,
                                           "next_link": paginator.get_next_link(),
                                           "previous_link": paginator.get_previous_link()}}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(data={"Exception": str(e)}, status=status.HTTP_200_OK)


class SellerProductRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serialized_data = serializer.data

        return Response(serialized_data)


class SellerProductUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class BrandAPIView(APIView):
    def get(self, request, format=None):
        try:
            brands = Brand.objects.all()
            serialized_brands = BrandSerializer(brands, many=True)
            return Response(serialized_brands.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class AllProducts:
    shared_products = None


class ProductFilter:
    myprod = Product.objects.exclude(Q(thumbnail_image__exact=''))
    myqueryset = Product.objects.exclude(Q(category_id__isnull=True))

    def __init__(self, queryset=None) -> None:

        self.queryset = queryset

    def get_queryset(self):
        return self.myqueryset

    def get_queryset_values(self):
        return self.myqueryset.values(
            "id", "thumbnail_image", "cost", "title", "description")

    def methods(self, qset=None, request=None):
        all_products = qset if qset else self.myqueryset
        print("method called")
        # categories = all_products.exclude(category__category_name="", category__category_name__isnull=True).values(
        #    "category__id", "category__category_name", "category__parent_id__category_name").distinct()
        categories = all_products.exclude(category__category_name="", category__category_name__isnull=True).values(
            "category__id", "category__category_name", "category__parent_id__category_name").distinct()
        # parent = all_products.exclude(category__category_name="", category__category_name__isnull=True).filter(
        #     category__id__in=all_products.exclude(category__category_name="", category__category_name__isnull=True).values_list(
        #         "category__parent_id__id", flat=True)).values(
        #     "category__id", "category__category_name", "category__parent_id__category_name").distinct()
        parent = all_products.exclude(category__category_name="", category__category_name__isnull=True).filter(category__id__in=all_products.exclude(category__category_name="", category__category_name__isnull=True).values_list(
            "category__parent_id__id", flat=True))
        print("parent", parent, all_products.exclude(category__category_name="", category__category_name__isnull=True).values_list(
            "category__category_name", flat=True).distinct())

        brands = all_products.exclude(Q(brand__brand_name=None) | Q(brand=None)).values(
            "brand__brand_name", "brand__id").distinct()

        price = all_products.aggregate(Max("cost"), Min('cost'))
        return {"filters": {"categories": categories, "brands": brands,  "price": price}}

    def get_user_wishlist(self, request):
        wishlist_items = None
        if request.user.is_authenticated:
            wishlist_items = ProductWishlist.objects.filter(
                user=request.user, product__in=self.myqueryset)
        else:
            wishlist_items = ProductWishlist.objects.none()
        wishlist_serializer = WishlistSerializer(
            wishlist_items, many=True).data
        wl_item = [ws['product']['id'] for ws in wishlist_serializer]
        return wl_item

    def dyanmic_filters(self, keysdict):
        print(1)
        filters = Q()  # Initialize an empty Q object for filtering
        if keysdict.get("brands"):
            print("BRAND FILTER")
            filters &= Q(brand__id__in=keysdict["brands"])

        print(1)

        if keysdict.get("categories"):
            print("CATEGORIES FILTER")
            filters &= Q(category__id__in=keysdict["categories"])

        print(1)

        price_range = keysdict.get("price_range")
        if price_range and price_range['max'] is not None:
            if price_range['min'] is not None:
                print("PRICE RANGE FILTER")
                filters &= Q(
                    cost__gte=price_range['min'], cost__lte=price_range['max'])
            else:
                print("PRICE MAX RANGE FILTER")
                filters &= Q(cost__lte=price_range['max'])

        print(1)

        if keysdict.get("brand"):
            print("RATING FILTER")
            filters &= Q(brand__id__in=keysdict["brand"])

        # Apply the dynamic filters to the queryset
        products = products.filter(filters)

        return products.order_by("id")

    def apply_filters(self, data):
        filtered_products = ProductFilter.myqueryset
        if ('brands' in data) and (data['brands'] != []):
            filtered_products = filtered_products.filter(
                brand__in=data['brands'])
            ProductFilter.myqueryset = filtered_products
        else:
            ProductFilter.myqueryset = self.myprod
        return filtered_products

    def filtering_products(self, products, keysdict):
        print(1)
        if ("brands" in keysdict) and (keysdict["brands"] != []) and (keysdict["brands"] is not None):
            print("BRAND FILTER")
            products = products.filter(brand__id__in=keysdict["brands"])
        print(1)
        if ("categories" in keysdict) and (keysdict["categories"] != []) and (keysdict["categories"] is not None):
            print("CATEGORIES FILTER")
            products = products.filter(brand__id__in=keysdict["categories"])
        print(1)

        if ("price_range" in keysdict) and (keysdict["price_range"]['max'] is not None):
            print("PRICE MAX RANGE FILTER")
            products = products.filter(
                Q(cost__lte=keysdict["price_range"]['max']))
        print(1)
        if ("price_range" in keysdict) and (keysdict["price_range"]['max'] is not None) and (keysdict["price_range"]['min'] is not None):
            print("PRICE RANGE FILTER")
            products = products.filter(
                Q(cost__gte=keysdict["price_range"]['min'], cost__lte=keysdict["price_range"]['max']))
        print(1)

        if ("brand" in keysdict) and (keysdict["brand"] != []) and (keysdict["brand"] is not None):
            print("RATING FILTER")

            products = products.filter(brand__id__in=keysdict["brand"])

        return {"products": products.order_by("id"), "products_count": products.count()}


class ShopCategoryAPIView(APIView):
    pf = ProductFilter()

    def post(self, request, *args, **kwargs):
        try:
            id = self.kwargs['id']
            # id = self.request.data["category_id"]
            print("category_id", id)
            if id is not None or id != '':
                paginator = MyCustomPagination()
                products = Product.objects.filter(
                    Q(category__parent_id=id) | Q(category=id)).all()
                # print("products.count() : ", Product.objects.filter(
                #     category__parent_id=id).count())
                fil_methods = self.pf.methods(qset=products, request=request)
                mydata = self.pf.filtering_products(
                    products, self.request.data)
                paginated_products = paginator.paginate_queryset(
                    mydata['products'], self.request)
                serializer = ProductSerializer(
                    paginated_products, many=True).data
                return Response(data={"products": serializer, "filters": fil_methods, "total_count": mydata["products_count"],
                                      "page": {"total_page": paginator.page.paginator.num_pages,
                                               "current_page": paginator.page.number,
                                               'next_page_number': paginator.page.next_page_number() if paginator.page.has_next() else None,
                                               'previous_page_number': paginator.page.previous_page_number() if paginator.page.has_previous() else None,
                                               "next_link": paginator.get_next_link(),
                                               "previous_link": paginator.get_previous_link()}}, status=status.HTTP_200_OK)
            else:
                return Response(data={"products": "No data of this category"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={"Exception": str(e)}, status=status.HTTP_200_OK)


class HomeShopAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            paginator = PageNumberPagination()
            categories_count = Product.objects.exclude(Q(category=None)).values(
                "category__parent_id__id", "category__parent_id__category_name", "category__category_name", "category__id").annotate(product_count=Count('id')).order_by("-product_count").filter(product_count__gte=20)

            prod = Product.objects.exclude(Q(thumbnail_image=None) | Q(category=None) | Q(thumbnail_image="")).annotate(
                product_count=Count('id')
            ).order_by("-id").values(
                "id", "thumbnail_image", "image_url", "name", "product_count"
            )

            return Response(data={"categories_count": categories_count, "prod": prod, }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={"Exception": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ShopView(APIView):
    pf = ProductFilter()

    def get(self, request, *args, **kwargs):
        try:

            paginator = MyCustomPagination()
            fil_prod = self.pf.myqueryset
            fil_methods = self.pf.methods()
            results = paginator.paginate_queryset(
                queryset=fil_prod, request=request)
            wl_items = self.pf.get_user_wishlist(request)
            print("len(results):", len(results))
            # print(paginator.get_next_link(),
            #       paginator.get_previous_link(),
            #       paginator.get_schema_operation_parameters,
            #       )

            serialized_data = ProductSerializer(results, many=True).data

            response_data = {
                "fil_prod": serialized_data,
                "wl_items": wl_items,
                "filters": fil_methods,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "schema_operation_parameters": paginator.get_schema_operation_parameters(view=self)
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            return Response(data={'Exception': error_message}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:

            paginator = MyCustomPagination()

            fil_methods = self.pf.methods(request=request)
            mydata = self.pf.filtering_products(
                self.pf.myqueryset, self.request.data)

            print(self.request.data)
            results = paginator.paginate_queryset(
                queryset=mydata["products"], request=request)
            print("paga_no : ", paginator.get_page_number(request, 2))
            wl_items = self.pf.get_user_wishlist(request)
            print("len(results):", len(results))
            serialized_data = ProductSerializer(results, many=True).data
            response_data = {
                "total_count": mydata["products_count"],
                "fil_prod": serialized_data,
                "wl_items": wl_items,
                "filters": fil_methods,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "schema_operation_parameters": paginator.get_schema_operation_parameters(view=self)
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            error_message = str(e)
            return Response(data={'Exception': error_message}, status=status.HTTP_200_OK)


class SellerHomePageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        user = self.request.user.id
        products = Product.objects.filter()
        return Response(data={"products": {"total": 0, "active": 0, "sold": 0}}, status=status.HTTP_200_OK)

