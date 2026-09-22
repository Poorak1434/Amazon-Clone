from .models import Cart, Category

def cart_context(request):
    cart_count = 0
    cart_obj = None
    
    if request.user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user).first()
    else:
        session_id = request.session.session_key
        if session_id:
            cart_obj = Cart.objects.filter(session_id=session_id).first()
            
    if cart_obj:
        cart_count = cart_obj.total_items
        
    categories = Category.objects.all()
    
    return {
        'global_cart_count': cart_count,
        'all_categories': categories,
        'user_pincode': request.session.get('user_pincode', '131021'),
        'user_city': request.session.get('user_city', 'Sonipat'),
        'user_name': request.session.get('user_name', request.user.first_name or request.user.username if request.user.is_authenticated else 'Poorak')
    }
