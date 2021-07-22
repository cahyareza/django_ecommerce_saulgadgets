from django.conf import settings

from apps.store.models import Product

class Cart(object):
    '''
    Akan membuat session dengan keys cart dan salah satu valuenya product_id
    "cart" ={
    "product_id": {
        'quantity': 0,
        'price': $9.99,
        'id': nike
        }
    }

    Kemudian pada session ini bisa menambahkan di session cart menggunakan prinsip2 dictionary data type
    '''

    def __init__(self, request):
        self.session = request.session
        # initialize session cart
        cart = self.session.get(settings.CART_SESSION_ID)

        # jika tidak bukan cart
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        # session cart keys adalah id
        product_ids = self.cart.keys()

        # data id dibuat list
        product_clean_ids = []

        # untuk mendapatkan product yang sesuai di data base dengan yang di POST di web console(Network)
        for p in product_ids:
            # memasukan data id ke list
            product_clean_ids.append(p)

            # mengambil data sesuai session dengan database dengan parameter p
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        # untuk mencari total
        for item in self.cart.values():
            item['total_price'] = float(item['price']) * int(item['quantity'])

            yield item

    #menjumlahkan quantity
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity =1, update_quantity=False):
        product_id = str(product.id)
        price = str(product.price)

        #jika pada session cart tidak ada keys product_id maka dibuat
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price':price, 'id': product_id}

        #update quantity
        if update_quantity:
            self.cart[product_id]["quantity"] = quantity

        else:
            self.cart[product_id]["quantity"] = self.cart[product_id]["quantity"] + 1

        self.save()

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        # update session
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def get_total_length(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_cost(self):
        return sum(item['total_price'] for item in self.cart.values())