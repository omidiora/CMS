from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse
from .models import *
from .forms import OrderForm,CreateUserForm
from .filters  import  OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group

@unauthenticated_user
def registerpage(request):
    form=CreateUserForm(request.POST) 
    if form.is_valid():
        user=form.save()
        username=form.cleaned_data.get('username')
        group=Group.objects.get(name="customer")
        user.groups.add(group)
        Customer.objects.create(user=user)
        messages.success(request,'Account was created for' + username)
        return redirect('login')
    context={'form':form}
    return render(request,'accounts/register.html',context)

@unauthenticated_user
def loginpage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password is incorrect')
        
    context={}
    return render(request,'accounts/login.html',context)

def logoutuser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()
    total_customers=customers.count()
    total_orders=orders.count()

    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='pending').count()

    context={'orders':orders,'customers':customers,'total_orders':total_orders,'delivered':delivered,'pending':pending }

    
    return render(request,'accounts/dashboard.html',context )


@login_required(login_url='login')
@allowed_users (allowed_roles=['admins'])
def products(request):
    products=Product.objects.all()
    return render(request,'accounts/product.html',{'products':products})
      

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def customer(request,pk_test):
    customer=Customer.objects.get(id=pk_test) 
    orders=customer.order_set.all() 
    order_count=orders.count()
    myfilter=OrderFilter(request.GET,queryset=orders)
    orders=myfilter.qs

    context={'customer':customer,'orders':orders,'order_count':order_count,'myfilter':myfilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def createorder(request,pk):
    orderformset=inlineformset_factory(Customer,Order,fields=('product','status'))
    customer=Customer.objects.get(id=pk)
    formset=orderformset(queryset=Order.objects.none(),instance=customer)

#    form=OrderForm(initial={'customer':customer})
    if request.method=='POST':
        formset=orderformset(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def updateorder(request,pk):
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)

    if request.method=='POST':
        form=OrderForm(request.POST,instance=order)
        if form.is_valid(): 
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/order_form.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def deleteorder(request,pk):
    order=Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context={'item':order}
    return render(request,'accounts/delete.html',context)
 


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    orders=request.user.customer.order_set.all()

    total_orders=orders.count()

    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='pending').count()
  
    context={'orders':orders,'delivered':delivered,'pending':pending,'total_orders':total_orders}

    
    return render(request,'accounts/user.html',context)


