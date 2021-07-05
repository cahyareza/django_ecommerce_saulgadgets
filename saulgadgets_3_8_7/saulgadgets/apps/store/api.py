from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json

from apps.cart.cart import Cart

from .models import Product

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