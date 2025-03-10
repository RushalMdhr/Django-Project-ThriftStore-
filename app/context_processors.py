from .models import Cart, OrderedBy, UserProfile, Category
from django.db.models import Sum, Count
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

def base_context(request):
    if request.user.is_authenticated:
        try:
            userprofile = UserProfile.objects.filter(user=request.user).first()
            
            cart_count = Cart.objects.filter(user=request.user).count()
            order_count = OrderedBy.objects.filter(userprofile=userprofile, process=False).count()
            profile_pic = userprofile.profile_pic
            sellers = UserProfile.objects.filter(vendor=True)
            if userprofile.vendor:
                vendor = True
            else:
                vendor = False

        except Exception as e:
            profile_pic = 'profile_pics/null_pfp.jpg'
            cart_count = 0
            order_count = 0
            vendor = False
    else:
        cart_count = 0
        order_count = 0
        vendor = False
        profile_pic = 'profile_pics/null_pfp'
    categories = Category.objects.all()
    print(f'media/{profile_pic}')
    return {
        'cart_count': cart_count,
        'order_count': order_count,
        'categories': categories,
        'vendor': vendor,
        'profile_pic':profile_pic,
    }
