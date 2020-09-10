from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate,login,logout

from .models import *
from .forms import OrderForm,CreateUserForm
from .filters import OrderFilter

# Create your views here.
def registerpage(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form= CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user= form.cleaned_data.get('username')
            messages.success(request,'Account was created for '+ user)
            #! we grabbed the username from the form and then passed to the messages
            return redirect('login')

    context= {'form':form}
    return render(request,'accounts/register.html',context)
def loginpage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        # we are getting username and password from the form whare name='username' and name='password'
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Usernmae or password is incorrect')
    context= {}
    return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')



def home(request):
    orders= Order.objects.all()
    total_orders=orders.count()
    customers=Customer.objects.all()
    total_customers =customers.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()

    context={'customers':customers, 'orders':orders,'total_orders':total_orders,'total_customers':total_customers,
            'delivered':delivered,'pending':pending}
    return render(request,'accounts/dashboard.html',context)

def products(request):
    products=Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

def customer(request,pk_test):
    customer=Customer.objects.get(id=pk_test)
    orders=customer.order_set.all()
    order_count=orders.count()
    myFilter=OrderFilter(request.GET, queryset=orders)
    orders= myFilter.qs
    context={'customer':customer,'orders':orders,'order_count':order_count, 'myFilter':myFilter}
    return render(request,'accounts/customer.html',context)


def createorder(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    #extra 10 is used to use 10 more extra fields for the form

    #for formset you have to insert parent model and the chiild model
    customer=Customer.objects.get(id=pk)
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # form = OrderForm(initial={'customer':customer})
    #customer value will be alredy filled up  in the form
    if request.method == 'POST':
        # form=OrderForm(request.POST)
        formset=OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)


def updateorder(request,pk):
    order=Order.objects.get(id=pk)
    if request.method == 'POST':
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    form = OrderForm(instance=order)
    context={'form':form}
    return render(request,'accounts/order_form.html',context)

def deleteorder(request,pk):
    order=Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request,'accounts/delete.html',context)