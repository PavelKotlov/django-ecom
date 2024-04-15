from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib import messages


def payment_success(request):
  return render(request, 'payment/payment_success.html', {})

def checkout(request):
  cart = Cart(request)
  cart_products = cart.get_products()
  quantities = cart.get_quantities()
  totals = cart.cart_total()

  if request.user.is_authenticated:
    shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    return render(request, "payment/checkout.html", {'cart_products':cart_products, 'product_quantities': quantities, 'totals': totals, 'shipping_form':shipping_form})
  else:
    shipping_form = ShippingForm(request.POST or None)
    return render(request, "payment/checkout.html", {'cart_products':cart_products, 'product_quantities': quantities, 'totals': totals, 'shipping_form':shipping_form})
  
def billing_info(request):
  if request.POST:
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    totals = cart.cart_total()

    my_shipping = request.POST 
    request.session['my_shipping'] = my_shipping

    if request.user.is_authenticated:
      billing_form = PaymentForm()

      return render(request, "payment/billing_info.html", {'cart_products':cart_products, 'product_quantities': quantities, 'totals': totals, 'shipping_info':request.POST, 'billing_form':billing_form})
    else:
      billing_form = PaymentForm()
      return render(request, "payment/billing_info.html", {'cart_products':cart_products, 'product_quantities': quantities, 'totals': totals, 'shipping_form':request.POST, 'billing_form':billing_form})
    
    shipping_form = request.POST
    return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})	
  
  else:
    messages.success(request, 'Access Denied.')
    return redirect('home')
  
def process_order(request):
  if request.POST:
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    totals = cart.cart_total()

    # Get Billing Info from the last page
    payment_form = PaymentForm(request.POST or None)
    # Get Shipping Session Data
    my_shipping = request.session.get('my_shipping')

    # Gather Order Info
    full_name = my_shipping['shipping_full_name']
    email = my_shipping['shipping_email']
    # Create Shipping Address from session info
    shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
    amount_paid = totals

    # Create an Order
    if request.user.is_authenticated:
      # logged in
      user = request.user
      # Create Order
      create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
      create_order.save()
      for product in cart_products:
              print(product)
              cart.delete(product.id)
      messages.success(request, "Order Placed!")
      return redirect('home')

    else:
      # not logged in
      # Create Order
      create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
      create_order.save()
      for product in cart_products:
        print(product)
        cart.delete(product.id)

      messages.success(request, "Order Placed!")
      return redirect('home')

  else:
    messages.success(request, "Access Denied")
    return redirect('home')