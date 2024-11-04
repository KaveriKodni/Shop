"""
URL configuration for flower_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from .Api_views import *

urlpatterns = [
    #     API URL

    path("Customer/", CustomerView.as_view(), name="Customer Data"),
    path("Customer/<int:id>", CustomerView.as_view(), name="Customer data by id"),
    path("Address/", AddressView.as_view(), name="Address"),
    path("Address/<int:id>", AddressView.as_view(), name="Address_using Id"),
    path("Flower/", FlowerView.as_view(), name="Flower"),
    path("Flower/id/<int:id>/", FlowerView.as_view(), name="GetFlowerById"),
    path("Flower/name/<str:name>/", FlowerView.as_view(), name="GetFlowerByName"),
    path("Category/", CategoriesView.as_view(), name="Category"),
    path("Category/id/<int:id>", CategoriesView.as_view(), name="CategoryBYID"),
    path("Category/name/<str:name>", CategoriesView.as_view(), name="CategoryByName"),
    path("Orders/", Orders.as_view(), name="Orders"),

    #     HTML VIEWS
    path('', home_page, name='home_page'),  # Ensure this matches your view and template
    path("shop/", shop_page.as_view(), name="shop_page"),
    path('contact/', ContactView.as_view(), name='contact_page'),
    path("Submit_page/",Submit_page,name="Submit_page"),
    path("Blog/", blog_page, name="blog_page"),
    path("AboutUs/", About_page, name="about_page"),
    path("Cart/", cart_page, name="cart_page"),
    path("Order/", Order_view.as_view(), name="Order_page"),
    path("flower_view/", flower_view.as_view(), name="flower_view"),


]
