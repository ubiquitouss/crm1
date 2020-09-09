from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm

# Create your views here.

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
    context={'customer':customer,'orders':orders,'order_count':order_count}
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