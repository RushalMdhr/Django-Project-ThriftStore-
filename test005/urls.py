from django.contrib import admin
from django.urls import path,include
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from payment import urls as payment_urls

urlpatterns = [
    path('payment/', include('payment.urls')),
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('categories/<str:category_name>',categories,name='categories'),
    path('overview/<int:id>',product_overview,name='product_overview'),

    path('login',login_page,name='login_page'),
    path('logout',logout_page,name='logout_page'),
    path('register',register_page,name='register_page'),
    path('profile/<int:id>',profile_page,name='profile'),

    path('upload',upload_page,name='upload_page'),
    path('vendor',vendor_page,name='vendor_page'),
    path('edit_product/<int:id>',edit_product,name='edit_product'),
    path('delete_product/<int:id>',delete_product,name='delete_product'),

    path('add_group/<str:table_name>/<int:id>',add_to_group,name='add_to_group'),
    path('remove/<str:table_name>/<int:id>',remove_from_group,name='remove_from_group'),
    path('cart',cart_page,name='cart_page'),
    path('update_cart/', update_cart, name='update_cart'),
    path('fav_page',fav_page,name='fav_page'),

    path('about_us',about_us,name='about_us'),
    path('contact',contact_page,name='contact'),
    path('FAQS',faqs_page,name='FAQS'),
    path('policy',policy_page,name='policy'),
    path('browse/<str:hashtag>',browse,name='browse'),

    path('checkout/<int:id>',checkout_page,name='checkout_page'),
    path('my_orders',order_page,name='my_orders'),
    path('update_quantity/<int:cart_id>',update_quantity,name='update_quantity'),
    
    path('send_email',send_email,name='send_email'),


]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,
                    document_root = settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()