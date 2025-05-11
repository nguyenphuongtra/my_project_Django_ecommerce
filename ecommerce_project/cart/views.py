from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product

def cart_detail(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    context = {
        'cart_items': products,
        'total': total,
    }
    return render(request, 'cart/cart_detail.html', context)

def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        try:
            qty = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            qty = 1

        product = get_object_or_404(Product, pk=product_id)
        if qty < 1:
            qty = 1
        elif qty > product.stock:
            qty = product.stock

        current = cart.get(str(product_id), 0)
        cart[str(product_id)] = current + qty

        request.session['cart'] = cart

    return redirect('cart:cart_detail')

def add_to_cart_buy_now(request, product_id):
    if request.method == 'POST':
        cart = {}
        
        try:
            qty = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            qty = 1

        product = get_object_or_404(Product, pk=product_id)
        if qty < 1:
            qty = 1
        elif qty > product.stock:
            qty = product.stock

        cart[str(product_id)] = qty
        
        request.session['cart'] = cart
        
        return redirect('orders:checkout')
        
    return redirect('cart:cart_detail')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('cart:cart_detail')

def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            cart.pop(str(product_id), None)
        request.session['cart'] = cart
    return redirect('cart:cart_detail')
