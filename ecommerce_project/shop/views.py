import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.db.models import Q, Count, Avg
from .models import Product, Category, Review, ReviewPhoto
from .forms import ReviewForm
import google.generativeai as genai
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)

chat_model = genai.GenerativeModel('models/gemini-1.5-pro')


def product_list(request, category_id=None):
    products = Product.objects.all()
    category = None
    categories = Category.objects.all()
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)
    
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'popular':
        products = products.annotate(review_count=Count('reviews')).order_by('-review_count')
    
    paginator = Paginator(products, 9)  
    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    
    return render(request, 'shop/product_list.html', {
        'products': products_page,
        'category': category,
        'categories': categories,
        'paginator': paginator,
        'page_obj': products_page,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product)
    sort_by = request.GET.get('sort', 'newest')
    rating_filter = request.GET.get('rating')
    has_photos = request.GET.get('has_photos')
    
    if sort_by == 'newest':
        reviews = reviews.order_by('-created_at')
    elif sort_by == 'highest':
        reviews = reviews.order_by('-rating')
    elif sort_by == 'lowest':
        reviews = reviews.order_by('rating')
    elif sort_by == 'helpful':
        reviews = reviews.order_by('-helpful_votes')
    
    if rating_filter:
        reviews = reviews.filter(rating=rating_filter)
    
    if has_photos == 'true':
        reviews = reviews.filter(photos__isnull=False).distinct()
    elif has_photos == 'false':
        reviews = reviews.filter(photos__isnull=True)
    

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax and request.method == 'GET':
        html = render_to_string(
            'shop/partials/reviews_list.html',
            {'reviews': reviews, 'user': request.user}
        )
        return JsonResponse({
            'success': True,
            'html': html
        })
    

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            
           
            for i in range(1, 4):
                photo_field = f'photo{i}'
                if photo_field in request.FILES:
                    photo = request.FILES[photo_field]
                    ReviewPhoto.objects.create(review=review, image=photo)
            
          
            if is_ajax:
                
                reviews = Review.objects.filter(product=product).order_by('-created_at')
                html = render_to_string(
                    'shop/partials/reviews_list.html',
                    {'reviews': reviews, 'user': request.user}
                )
                return JsonResponse({
                    'success': True,
                    'html': html
                })
                
            return redirect('shop:product_detail', pk=product.pk)
        elif is_ajax:
            
            return JsonResponse({
                'success': False,
                'message': 'Thông tin không hợp lệ. Vui lòng kiểm tra lại.'
            })
    else:
        form = ReviewForm()
    
    
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(pk=product.pk)[:4]
    
    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'form': form,
    }
    return render(request, 'shop/product_detail.html', context)


def search_products(request):
    query = request.GET.get('q', '').strip()
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )
    else:
        products = Product.objects.none()
    
    paginator = Paginator(products, 9)  
    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    
    return render(request, 'shop/search_results.html', {
        'query': query,
        'products': products_page,
        'paginator': paginator,
        'page_obj': products_page,
    })


def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    
    sort_by = request.GET.get('sort_by', 'newest')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    else:  
        products = products.order_by('-created_at')
    
    paginator = Paginator(products, 9)  
    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    
    return render(request, 'shop/category_products.html', {
        'selected_category': category,
        'products': products_page,
        'categories': categories,
        'paginator': paginator,
        'page_obj': products_page,
    })


def home_view(request):
    featured_products = Product.objects.all()[:4]
    trending_products = Product.objects.all()[:8]
    categories = Category.objects.all()
    return render(request, 'shop/home.html', {
        'featured_products': featured_products,
        'trending_products': trending_products,
        'categories': categories,
    })

def contact_view(request):
    context = {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'shop/contact.html', context)

def about_view(request):
    return render(request, 'shop/about.html')

def chatbot_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            
            conversation_history = request.session.get('chat_history', [])
            
            if not user_message:
                return JsonResponse({'error': 'Tin nhắn trống'}, status=400)

            response_data = process_chatbot_message(request, user_message, conversation_history)
            
            conversation_history.append({"user": user_message, "bot": response_data['response']})
            conversation_history = conversation_history[-10:]
            request.session['chat_history'] = conversation_history
            
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dữ liệu JSON không hợp lệ'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    if 'chat_history' not in request.session:
        request.session['chat_history'] = []
        
    return render(request, 'shop/chatbot.html')

def process_chatbot_message(request, user_message, conversation_history):
    """Process user message and generate appropriate response"""
    
    def format_price_vnd(price):
        try:
            numeric_value = float(price)
            formatted_value = "{:,.0f}".format(numeric_value).replace(',', '.')
            return f"{formatted_value}₫"
        except (ValueError, TypeError):
            return str(price)
    
    conversation_context = "\n".join([
        f"User: {exchange['user']}\nBot: {exchange['bot']}" 
        for exchange in conversation_history
    ])
    
    intent = detect_intent(user_message.lower())
    
    context_info = ""
    
    if intent == "product_inquiry":
        products = get_matching_products(user_message)
        if products:
            product_info = "\n".join([
                f"{p.name}: {format_price_vnd(p.price)} - {p.description[:100]}..." 
                for p in products
            ])
            context_info = f"Thông tin sản phẩm:\n{product_info}"
        else:
            context_info = "Không tìm thấy sản phẩm phù hợp với yêu cầu."
    
    elif intent == "category_inquiry":
        categories = Category.objects.all()
        category_info = "\n".join([f"- {category.name}" for category in categories])
        context_info = f"Danh mục sản phẩm:\n{category_info}"
    
    elif intent == "price_inquiry":
        products = get_matching_products(user_message)
        if products:
            product_info = "\n".join([
                f"{p.name}: {format_price_vnd(p.price)}" 
                for p in products
            ])
            context_info = f"Thông tin giá:\n{product_info}"
    
    elif intent == "stock_inquiry":
        products = get_matching_products(user_message)
        if products:
            product_info = "\n".join([
                f"{p.name}: {p.stock} sản phẩm còn lại" 
                for p in products
            ])
            context_info = f"Thông tin tồn kho:\n{product_info}"
    

    prompt = f"""
Bạn là trợ lý mua sắm cho cửa hàng thương mại điện tử.
Lịch sử cuộc trò chuyện:
{conversation_context}

Tin nhắn mới nhất của người dùng: {user_message}

Thông tin liên quan:
{context_info}

Hãy trả lời ngắn gọn, lịch sự và hữu ích. Nếu bạn không biết thông tin, hãy đề nghị người dùng liên hệ với cửa hàng qua trang liên hệ.
"""

    session = chat_model.start_chat()
    response = session.send_message(prompt)
    bot_text = response.text
    
    return {'response': bot_text}

def detect_intent(message):
    """Detect the user's intent from their message"""
    if any(keyword in message for keyword in ["sản phẩm", "hàng", "mua", "bán"]):
        return "product_inquiry"
    elif any(keyword in message for keyword in ["danh mục", "loại", "phân loại"]):
        return "category_inquiry"
    elif any(keyword in message for keyword in ["giá", "bao nhiêu", "chi phí"]):
        return "price_inquiry"
    elif any(keyword in message for keyword in ["còn hàng", "tồn kho", "số lượng"]):
        return "stock_inquiry"
    else:
        return "general_inquiry"

def get_matching_products(message):
    """Find products that match keywords in the user message"""
    words = message.lower().split()
    query = Q()
    for word in words:
        if len(word) > 2: 
            query |= Q(name__icontains=word) | Q(description__icontains=word)
    
    products = Product.objects.filter(query)
    
    if not products:
        return Product.objects.all()[:3]
    
    return products[:5]  

@login_required
@require_POST
def vote_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.helpful_votes += 1
    review.save()
    return JsonResponse({'success': True, 'votes': review.helpful_votes})

@login_required
@require_POST
def report_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.reported = True
    review.save()
    return JsonResponse({'success': True})