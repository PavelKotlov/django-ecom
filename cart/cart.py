class Cart():
  def __init__(self, request):
    self.session = request.session

    # Retrieve current session key if exists
    cart = self.session.get('session_key')

    if 'session_key' not in request.session:
      cart = self.session['session_key'] = {}
    pass