from django.urls import path
from . import views

urlpatterns = [
    
    path('register',views.registerpage,name='register'),
    path('login',views.loginpage,name='login'),
    path('logout',views.logoutuser,name='logout'),

    path('',views.home ,name='home'),
    
    path('user/',views.userpage,name='user-page'),

    path('product',views.products,name='products'),
    path('customer/<str:pk_test>/',views.customer,name="customer") ,
    path('createorder/<str:pk>/',views.createorder,name="createorder"),
    path('update/<str:pk>/',views.updateorder,name="updateorder"),
    path('delete/<str:pk>/',views.deleteorder,name="deleteorder"),


]