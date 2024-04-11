from store.models import Product

class Cart():
  def __init__(self, request):
    self.session = request.session

    # Retrieve current session key if exists
    cart = self.session.get('session_key')

    # If no session key present create one
    if 'session_key' not in request.session:
      cart = self.session['session_key'] = {}
    
    # Make cart avaialble on all pages
    self.cart = cart

  def add(self, product, cart_quantity):
    product_id = str(product.id)
    product_qty = str(cart_quantity)

    if product_id not in self.cart:
      self.cart[product_id] = int(product_qty)

    self.session.modified = True

  def __len__(self):
    return len(self.cart)
  
  def get_products(self):
    product_ids = self.cart.keys()

    products = Product.objects.filter(id__in=product_ids)

    return products
  
  def get_quantities(self):
    quantities = self.cart
    return quantities