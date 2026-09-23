from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Avg, Count
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Category, Product, ProductImage, Address, Cart, CartItem, Order, OrderItem, Review, Banner


def get_or_create_cart(request):
    """Helper function to obtain cart linked to user or session."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_id=session_id)
    return cart


def home_view(request):
    categories = Category.objects.all()
    deal_products = Product.objects.filter(is_deal_of_the_day=True)[:8]
    prime_deals = Product.objects.filter(is_prime=True)[:8]
    featured_products = Product.objects.all()[:12]
    hero_banner = Banner.objects.filter(is_active=True).first()

    # Specific showcase items for Amazon homepage cards
    starting_399 = Product.objects.filter(price__lte=1000)[:4]
    alexa_items = Product.objects.filter(category__slug='smart-home')[:4]
    smart_rings = Product.objects.filter(title__icontains='Ring') | Product.objects.filter(category__slug='electronics')[:4]
    samsung_tv = Product.objects.filter(title__icontains='Samsung').first()

    context = {
        'categories': categories,
        'deal_products': deal_products,
        'prime_deals': prime_deals,
        'featured_products': featured_products,
        'starting_399': starting_399,
        'alexa_items': alexa_items,
        'smart_rings': smart_rings,
        'samsung_tv': samsung_tv,
        'hero_banner': hero_banner,
    }
    return render(request, 'store/home.html', context)


@require_POST
def add_review_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    title = request.POST.get('title', 'Great product').strip()
    rating = int(request.POST.get('rating', 5))
    comment = request.POST.get('comment', '').strip()
    
    # Use authenticated user or fallback user
    user = request.user if request.user.is_authenticated else User.objects.filter(is_staff=True).first()
    if not user:
        user = User.objects.create(username="customer_" + str(request.session.session_key[:6]))

    Review.objects.create(
        product=product,
        user=user,
        title=title,
        rating=rating,
        comment=comment,
        verified_purchase=True
    )
    messages.success(request, "Thank you! Your customer review has been published.")
    return redirect('product_detail', slug=product.slug)


def product_list_view(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    prime_only = request.GET.get('prime') == '1'
    sort_by = request.GET.get('sort', 'featured')

    products = Product.objects.all()
    selected_category = None

    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__name__icontains=query)
        )

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    if prime_only:
        products = products.filter(is_prime=True)

    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

    categories = Category.objects.all()

    context = {
        'products': products,
        'query': query,
        'selected_category': selected_category,
        'categories': categories,
        'sort_by': sort_by,
        'prime_only': prime_only,
        'result_count': products.count(),
    }
    return render(request, 'store/product_list.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:6]
    reviews = product.reviews.all()

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
    }
    return render(request, 'store/product_detail.html', context)


@require_POST
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_count': cart.total_items,
            'message': f'Added {product.title[:25]}... to your cart.'
        })

    messages.success(request, f'Added "{product.title}" to your Shopping Cart.')
    return redirect('cart')


def update_cart_view(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            cart = cart_item.cart
            return JsonResponse({
                'status': 'success',
                'cart_count': cart.total_items,
                'subtotal': float(cart.subtotal),
                'total_savings': float(cart.total_savings)
            })

    return redirect('cart')


def remove_from_cart_view(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect('cart')


def cart_view(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()
    
    # Calculate free delivery threshold (e.g. Free delivery over ₹499)
    free_delivery_eligible = cart.subtotal >= 499 or any(item.product.is_prime for item in cart_items)
    amount_needed_for_free_delivery = max(0, 499 - float(cart.subtotal)) if not free_delivery_eligible else 0

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'free_delivery_eligible': free_delivery_eligible,
        'amount_needed': amount_needed_for_free_delivery,
    }
    return render(request, 'store/cart.html', context)


def checkout_view(request):
    cart = get_or_create_cart(request)
    if cart.total_items == 0:
        messages.warning(request, "Your cart is empty! Add items before checkout.")
        return redirect('home')

    user_address = None
    if request.user.is_authenticated:
        user_address = Address.objects.filter(user=request.user, is_default=True).first() or Address.objects.filter(user=request.user).first()

    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
        'address': user_address,
    }
    return render(request, 'store/checkout.html', context)


@require_POST
def place_order_view(request):
    cart = get_or_create_cart(request)
    if cart.total_items == 0:
        return redirect('home')

    full_name = request.POST.get('full_name', 'Poorak Pandey')
    email = request.POST.get('email', 'poorak@example.com')
    mobile = request.POST.get('mobile', '+91 9876543210')
    pincode = request.POST.get('pincode', '131021')
    city = request.POST.get('city', 'Sonipat')
    state = request.POST.get('state', 'Haryana')
    address_line = request.POST.get('address_line', 'House No 42, Sector 15')
    payment_method = request.POST.get('payment_method', 'Amazon Pay Balance / UPI')

    full_shipping_address = f"{full_name}, {address_line}, {city}, {state} - {pincode}. Mobile: {mobile}"

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        full_name=full_name,
        email=email,
        mobile=mobile,
        shipping_address=full_shipping_address,
        payment_method=payment_method,
        total_amount=cart.subtotal,
        status='Ordered'
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_title=item.product.title,
            product_image=item.product.main_image,
            price=item.product.price,
            quantity=item.quantity
        )

    # Empty the cart
    cart.items.all().delete()

    messages.success(request, f"Order placed successfully! Order ID: #{order.order_id}")
    return render(request, 'store/order_success.html', {'order': order})


def orders_view(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        orders = Order.objects.all()[:5]

    return render(request, 'store/orders.html', {'orders': orders})


@require_POST
def set_location_view(request):
    pincode = request.POST.get('pincode', '131021').strip()
    city = request.POST.get('city', 'Sonipat').strip()
    
    request.session['user_pincode'] = pincode if pincode else '131021'
    request.session['user_city'] = city if city else 'Sonipat'
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'pincode': request.session['user_pincode'], 'city': request.session['user_city']})

    return redirect(request.META.get('HTTP_REFERER', '/'))


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Amazon.in, {user.username}!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect('home')
