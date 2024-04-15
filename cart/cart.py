from store.models import Product, Profile

class Cart():
  def __init__(self, request):
    self.session = request.session
    self.request = request

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

    # Cart persistance
    if self.request.user.is_authenticated:
      # If user is authenticated grab the user profile
      current_user = Profile.objects.filter(user__id=self.request.user.id)
      # Grab the cart items convert them to str and prep for JSON
      cart = str(self.cart)
      cart = cart.replace("\'", "\"")
      # Update old cart field in user profile with a str of cart items in dict format
      current_user.update(old_cart=cart)
    
  def cart_total(self):
    product_ids = self.cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    quantitites = self.cart
    total = 0

    for key, value in quantitites.items():
      key = int(key)
      for product in products:
        if product.id == key:
          if product.is_sale:
            total = total + (product.sale_price * value)
          else:
            total = total + (product.price * value)

    return total

  def __len__(self):
    return len(self.cart)
  
  def get_products(self):
    product_ids = self.cart.keys()

    products = Product.objects.filter(id__in=product_ids)

    return products
  
  def get_quantities(self):
    quantities = self.cart
    return quantities
  
  def update(self, product, quantity):
    product_id = str(product)
    product_qty = int(quantity)

    ourcart = self.cart

    ourcart[product_id] = product_qty

    self.session.modified = True

    ourcart = self.cart
    return ourcart
  
  def delete(self, product):
    product_id = str(product)

    if product_id in self.cart:
      del self.cart[product_id]
    
    self.session.modified = True
  