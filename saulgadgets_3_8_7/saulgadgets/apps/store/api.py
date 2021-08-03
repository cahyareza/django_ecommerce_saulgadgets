from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
import json

from apps.cart.cart import Cart

from apps.orders.utils import checkout

from .models import Product
from apps.orders.models import Order

def api_checkout(request):
    cart = Cart(request)

    data = json.loads(request.body)
    jsonresponse = {'success': True}
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    address = data['address']
    zipcode = data['zipcode']
    place = data['place']

    orderid = checkout(request, first_name, last_name, email, address, zipcode, place)

    #ini buat ngetest aja apakah ilang tidak jika paid true cartnya
    paid = True

    if paid == True:
        order = Order.objects.get(pk=orderid)
        order.paid = True
        order.paid_amount = cart.get_total_cost()
        order.save()

        cart.clear()

    return JsonResponse(jsonresponse)

def api_add_to_cart(request):
    # JSON.loads, parse a valid JSON string and convert it to python dictionary
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    # get value of dictionary
    product_id = data['product_id']
    update = data['update']
    quantity = data['quantity']

    # initialize objects cart
    cart = Cart(request)

    # get same product as json load
    product = get_object_or_404(Product, pk=product_id)

    if not update:
        # use method in Cart class
        cart.add(product=product, quantity=1, update_quantity=False)

    else:
        cart.add(product=product, quantity=quantity, update_quantity=True)

    # convert dictionary to JSON string
    return JsonResponse(jsonresponse)

def api_remove_from_cart(request):
    # JSON.loads, parse a valid JSON string and convert it to python dictionary
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    # get value of dictionary
    product_id = str(data['product_id'])

    # initialize objects cart
    cart = Cart(request)

    cart.remove(product_id)

    return JsonResponse(jsonresponse)