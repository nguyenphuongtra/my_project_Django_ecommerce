from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Order, OrderItem
from django.http import JsonResponse
from .models import Order, OrderItem, Province, District, Ward
from .models import ORDER_STATUS, PAYMENT_METHODS
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404


def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0')
    
    for product_id, quantity in cart.items():
        try:
            quantity = int(quantity)
            product = get_object_or_404(Product, id=product_id)
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except:
            continue
    
    if request.method == 'POST':
        prov_code = request.POST.get('province', '').strip()
        dist_code = request.POST.get('district', '').strip()
        ward_code = request.POST.get('ward', '').strip()
        shipping_address = request.POST.get('shipping_address', '').strip()
        payment_method = request.POST.get('payment_method')

        province = Province.objects.filter(code=prov_code).first() if prov_code else None
        district = District.objects.filter(code=dist_code).first() if dist_code else None
        ward     = Ward.objects.filter(code=ward_code).first()     if ward_code else None

        shipping_fee = Decimal('30000')
        order_total = Decimal('0')

        order = Order.objects.create(
            user=request.user,
            payment_method=payment_method,
            province=province,
            district=district,
            ward=ward,
            shipping_address=shipping_address,
            shipping_fee=shipping_fee,
            total=order_total,
        )

        for pid, qty_str in cart.items():
            try:
                qty = int(qty_str)
            except:
                continue
            if qty <= 0:
                continue
            product = get_object_or_404(Product, id=pid)
            subtotal = product.price * qty
            order_total += subtotal

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                price=product.price,
            )

        order.total = order_total + shipping_fee
        order.save()

        request.session['cart'] = {}
        return redirect('orders:order_history')

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

def get_districts(request, province_id):
    districts = District.objects.filter(province_id=province_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)


def districts_json(request):
    province_code = request.GET.get('province')
    qs = District.objects.filter(province__code=province_code)
    data = [{'code': d.code, 'name': d.name_with_type} for d in qs]
    return JsonResponse(data, safe=False)

def wards_json(request):
    district_code = request.GET.get('district')
    qs = Ward.objects.filter(district__code=district_code)
    data = [{'code': w.code, 'name': w.name_with_type} for w in qs]
    return JsonResponse(data, safe=False)

@login_required
def order_detail_api(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        items = []
        subtotal = Decimal('0')
        
        for item in order.items.all():
            item_subtotal = item.price * item.quantity
            subtotal += item_subtotal
            
            items.append({
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': float(item.price),
                'price_formatted': f"{item.price:,}".replace(',', '.') + ' đ',
                'subtotal': float(item_subtotal),
                'subtotal_formatted': f"{item_subtotal:,}".replace(',', '.') + ' đ',
            })
        
        province_name = order.province.name_with_type if order.province else ''
        district_name = order.district.name_with_type if order.district else ''
        ward_name = order.ward.name_with_type if order.ward else ''
        
        payment_methods_dict = dict(PAYMENT_METHODS)
        payment_method_display = payment_methods_dict.get(order.payment_method, order.payment_method)
        
        status_dict = dict(ORDER_STATUS)
        status_display = status_dict.get(order.status, order.status)
        
        created_at_formatted = order.created_at.strftime('%d/%m/%Y %H:%M')
        
        try:
            shipping_fee = Decimal(order.shipping_fee) if order.shipping_fee else Decimal('0')
            total = Decimal(order.total) if order.total else Decimal('0')
            
            if total <= 0 or total < subtotal:
                total = subtotal + shipping_fee
        except InvalidOperation:
            shipping_fee = Decimal('0')
            total = subtotal + shipping_fee
        
        order_data = {
            'id': order.id,
            'created_at': created_at_formatted,
            'status': order.status,
            'status_display': status_display,
            'payment_method': order.payment_method,
            'payment_method_display': payment_method_display,
            'shipping_address': order.shipping_address,
            'province_name': province_name,
            'district_name': district_name,
            'ward_name': ward_name,
            'shipping_fee': float(shipping_fee),
            'shipping_fee_formatted': f"{shipping_fee:,}".replace(',', '.') + ' đ',
            'subtotal': float(subtotal),
            'subtotal_formatted': f"{subtotal:,}".replace(',', '.') + ' đ',
            'total': float(total),
            'total_formatted': f"{total:,}".replace(',', '.') + ' đ',
            'items': items,
        }
        
        return JsonResponse(order_data)
    except InvalidOperation as e:
        return JsonResponse({'error': 'Invalid decimal value in order data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)