from django.urls import path
from . import views
from users.views import custom_logout

from django.urls import path
# from .views import search_products

urlpatterns = [
    # Product-related URLs
    path('', views.categories, name='categories'),
    path('<int:category_id>/products/', views.products, name='products'),
    path('all-products/', views.all_products, name='all_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.search_products, name='search_products'),
    
    # Authentication URL
    path('logout/', custom_logout, name='logout'),

    # path('search/', search_products, name='search_products'),
]