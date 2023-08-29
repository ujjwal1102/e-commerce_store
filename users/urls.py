
from django.urls import path
from . import views
from django.urls import path, include,re_path

urlpatterns = [
    path('faltu',views.faltu,name='faltu'),
    path('',views.IndexView.as_view(),name='index'),
    path('login',views.LoginView.as_view(),name='login'),
    path('<str:slug>/signup',views.SignUpView.as_view(),name='signup'),
    
    path('accounts',views.AccountsView.as_view(),name='accounts'),
    #============================================================================
    
    
    
    path('products-list',views.ProductsListView.as_view(),name='products_list'),
    path('products-grid',views.ProductsGridView.as_view(),name='products_grid'),
    path('product-detail/<str:id>/',views.ProductDetailView.as_view(),name='product_detail'),
    path('product-detail',views.ProductDetailView.as_view(),name='product_detail'),
    
    #==============================================================================
    
    path('add-new-product',views.AddProductView.as_view(),name='add_product'),
    
    #==========================================================================
    path('wishlist',views.WishlistView.as_view(),name='wishlist'),
    path('remove-item-wishlist',views.RemoveFromWishlist.as_view(),name='remove_from_wishlist'),
    #========================================================================
    path('cart',views.CartView.as_view(),name='cart'),
    path('add-to-cart',views.AddToCart.as_view(),name='add_to_cart'),
    path('dynamic',views.dynamicform.as_view(),name='dynamic'),
    path('remove-item/<str:id>',views.RemoveFromCart.as_view(),name='remove_item'),
    
    #========================================================================
    path('categories/',views.CategoriesListView.as_view(),name='categories_list'),
    path('categories/<str:id>',views.ShopByCategoryView.as_view(),name='shop_by_category'),
    # path('categories/all',views.CategoryView.as_view(),name='categories_all'),
    path('categories/category',views.CategoryView.as_view(),name='category'),
    path('categories/category/create',views.AddCategoryView.as_view(),name='create_category'),
    # path('categories/create/child-category',views.AddChildCategoryView.as_view(),name='create_child_category'),
    # path('categories/create/grant-child-category',views.AddGrantChildCategoryView.as_view(),name='create_grant_child_category'),
    path('categories/child-category/create',views.AddChildCategoryView.as_view(),name='create_child_category'),
    # path('categories/update/parent-category',views.AddCategoryView.as_view(),name='update_category'),
    # path('categories/update/child-category',views.AddCategoryView.as_view(),name='update_child_category'),
    path('categories/grant-child-category/create',views.AddGrantChildCategoryView.as_view(),name='create_grant_child_category'),
    
    # path('categories/delete/parent-category',views.AddCategoryView.as_view(),name='delete_category'),
    # path('categories/delete/child-category',views.AddCategoryView.as_view(),name='delete_child_category'),
    # path('categories/delete/grant-child-category',views.AddCategoryView.as_view(),name='delete_grant_child_category'),

    ###################################################
    path('search/',views.SearchView.as_view(),name="search_results"),
    # re_path(r'^$',views.IndexView.as_view(),name='index'),
    path('filter/',views.FilterView.as_view(),name='filter'),
    ################################################################
    path('profile',views.ProfileView.as_view(),name='profile'),
    path('profile/create',views.CreateProfileView.as_view(),name='create_profile'),
    path('profile/update',views.UpdateProfileView.as_view(),name='update_profile'),
    path('logout',views.LogoutView.as_view(),name='logout'),
]