from decimal import Decimal

from products.models import Product


class Cart:

    # Create Session

    def __init__(self, request):
        self.session = request.session
        self.coupon = None
        # Returning user - obtain her existing session
        cart = self.session.get('session_key')
        # New user - generate a new session
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

   # Apply coupon

    def apply_coupon(self, coupon_code):
        if coupon_code == 'IGUS':
            self.coupon = coupon_code

    # Remove coupon

    def remove_coupon(self):
        self.coupon = None

    # Get discount total

    def get_discounted_total(self):
        total = self.get_total()
        if self.coupon == 'IGUS':
            discount = Decimal('0.8')
            return total * discount
        return total

    # Add item to cart

    def add(self, product, product_qty, product_size):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty
            self.cart[product_id]['size'] = product_size
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty, 'size': product_size}
        self.session.modified = True

    # Delete item

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

    # Update cart

    def update(self, product, qty, size):
        product_id = str(product)
        product_quantity = qty
        product_size = size
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_quantity
            self.cart[product_id]['size'] = product_size
        self.session.modified = True

    # Output the amount item in the cart

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    # Output all products in the cart

    def __iter__(self):

        all_product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
            yield item

    # Total price

    def get_total(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())









