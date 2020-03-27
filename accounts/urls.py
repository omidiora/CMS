from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    path('register',views.registerpage,name='register'),
    path('login',views.loginpage,name='login'),
    path('logout',views.logoutuser,name='logout'),

    path('',views.home ,name='home'),
    
    path('user/',views.userpage,name='user-page'),

    path('account/',views.accountsettings,name='user-page'),

    path('product',views.products,name='products'),
    path('customer/<str:pk_test>/',views.customer,name="customer") ,
    path('createorder/<str:pk>/',views.createorder,name="createorder"),
    path('update/<str:pk>/',views.updateorder,name="updateorder"),
    path('delete/<str:pk>/',views.deleteorder,name="deleteorder"),

    path('resetpassword',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="reset_password" ),
    path('resetpasswordsent/',auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
    name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),name="password_reset_confirm"),
    path('resetpasswordcomplete',auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),name="password_reset_complete"),


]