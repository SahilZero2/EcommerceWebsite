from django.shortcuts import render
from django.http import HttpResponse
# from .models import Products,Order,OrderItem,Customer,ShippingAddress
from .models import *
from random import randint
from paytm.Checksum import generate_checksum
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
MERCHANT_KEY = 'bQfzzkKzeCbR7jOl'

def ProductsView(request):
    myprod = Products.objects.all()
    print(myprod)
    return render(request,'productView.html',{"myprod" : myprod})

def sendpaymentrequest(request,pk):
    
    product= Products.objects.get(pk = pk)
    param_dict = {
        'MID': 'amitgo59443067266036',
        'ORDER_ID': str(randint(10,99999999)), # order id 
        'TXN_AMOUNT': str(product.price), # amount demanded for.
        'CUST_ID': "mailtomeontushar@gmail.com",
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEB', # for demo purpose only.
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL':'http://127.0.0.1:8000/response/' # on this url paytm will send you the status of request
    }
    param_dict['CHECKSUMHASH'] = generate_checksum(param_dict,MERCHANT_KEY)
    return render(
        request,
        "process.html",
        {
            'paymentdetails':param_dict
        }
    )

@csrf_exempt
def responsefrompaytm(request):
    return render(
        request,
        "response.html",
        {
            'response':request.POST
        }
    )


def aboutus(request):
    return render(
        request,
        'about.html'
    )


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
    else:
        # empty cart for none-logged in users
        items =[]
        order = {'get_cart_total':0, 'get_cart_items':0 }
    context = {'items' : items , 'order' : order}

    return render(
        request,
        'cart.html',
        context
    )

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
    else:
        items =[]
        order = {'get_cart_total':0, 'get_cart_items':0 }
    context = {'items' : items , 'order' : order}

    return render(
        request,
        'checkout2.html',
        context
    )


