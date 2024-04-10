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

  def add(self, product):
    product_id = str(product.id)

    if product_id not in self.cart:
      self.cart[product_id] = {'price':str(product.price)}

    self.session.modified = True

  def __len__(self):
    return len(self.cart)