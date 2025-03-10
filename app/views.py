from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .utils import send_email_to_clint
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.db.models import Q, Count
import hashlib

def home(request):
    image_details = Product.objects.all()
    username = request.user.username
    search = request.GET.get('search')
    if request.GET.get('search'):
        image_details = image_details.filter(
            Q(product_name__icontains = search) |
            Q(category__category_name__icontains = search) |
            Q(product_description__icontains = '#'+ search)
        )
        search = True
    else:
        search=False
    
    paginator = Paginator(image_details, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : 'Home',
        'image_details' : page_obj,
        'username' : username,
        'search' : search,
    }
    
    return render(request,'home.html',context)

def categories(request,category_name):
    image_details = Product.objects.filter(category__category_name=category_name)

    paginator = Paginator(image_details, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)

    context = {
        'image_details' : page_obj,
        'search' : True
    }
    return render(request,'home.html',context)

def about_us(request):
    return render(request,'us/about_us.html')

def policy_page(request):
    return render(request,'us/policy.html')

def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(email)
        Feedback.objects.create(
            userprofile = UserProfile.objects.filter(user__email=email).first(),
            message = message
        )
        # send_email_to_clint(email)
    return render(request,'us/contact.html')

def faqs_page(request):
    return render(request,'us/faqs.html')

def profile_page(request,id):
    if request.method == 'POST':
        userprofile = UserProfile.objects.get(user=request.user)
        
        # Update user details
        userprofile.user.username = request.POST.get('username')
        userprofile.user.first_name = request.POST.get('first_name')
        userprofile.user.last_name = request.POST.get('last_name')
        userprofile.address = request.POST.get('address')
        
        # Check if a new profile picture was uploaded
        try:
            data = request.POST
            if request.FILES['profile_picture']:
                userprofile.profile_pic = request.FILES['profile_picture']
            else:
                print("No profile picture uploaded")
        except Exception as e:
            messages.error(request, f"Error updating profile picture: {e}")
        # Save the updated user profile and user object
        userprofile.user.save()  # Save changes to the user object
        userprofile.save()       # Save changes to the user profile
        return HttpResponseRedirect(request.path)
    try:
        userprofile = UserProfile.objects.get(user=User.objects.get(id=id))
    except Exception as e:
        userprofile = None

    context = {
        'userprofile' : userprofile,
    }
    return render(request,'profile/profile.html',context)

def browse(request,hashtag):
    image_details = Product.objects.filter(
            Q(product_name__icontains = hashtag) |
            Q(category__category_name__icontains = hashtag) |
            Q(product_description__icontains = '#'+ hashtag)
        )
    
    paginator = Paginator(image_details, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : 'Home',
        'image_details' : page_obj,
        'search' : True
    }
    return render(request,'home.html',context)


def login_page(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')


        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login')


        user = authenticate(username = username ,password = password)


        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login')
        else:
            login(request, user)
            return redirect('/')

    context = {
        'title' : 'LOGIN'
    }
    return render(request,'accounts/login.html',context)

def register_page(request):
    if request.method=="POST":
        try:
            first_name = request.POST.get('first name')
            last_name = request.POST.get('last name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirmPassword')
            if password == confirm_password:
                user = User.objects.filter(username = username)

                if user.exists():
                    messages.info(request, "username already exists")
                    return redirect('/register')

                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password
                )
                user.set_password(password)
                UserProfile.objects.create(
                    user=user,
                )
                user.save()
                messages.info(request, "Account created sucessfully")
                return redirect('/login')
            else:
                message.error(request,'Passwords Donot Match')
        except Exception as e:
            messages.error(request,f'error : {e}')

    return render(request,'accounts/register.html')

def logout_page(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login')
def upload_page(request):

    if request.method == 'POST':
        data = request.POST

        try:
            Product.objects.create(
                created_by=request.user,
                product_name=data.get('product_name'),
                product_description=data.get('product_description'),
                product_price=data.get('product_price'),
                product_rating=int(data.get('cond')),
                category=Category.objects.get(category_name = data.get('categories')),
            )
            for x in request.FILES.getlist('product_images'):
                print('imtage',x)
            print('product_images',)
            for image in request.FILES.getlist('product_images'):
                ProductImage.objects.create(
                    product=Product.objects.last(), 
                    image=image
                )
            # ProductImage.objects.create(
            #     product=Product.objects.last(), 
            #     image=request.FILES.get('product_image')
            # )
            messages.success(request, "Product uploaded successfully.")
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.products_uploaded += 1
            return HttpResponseRedirect(request.path)
        except Exception as e:
            messages.error(request, f"Error uploading product: {str(e)}")
            return HttpResponseRedirect(request.path)

        return redirect('/')

    options = Category.objects.all()
    context = {
        'categories' : options
    }
    return render(request,'vendor/upload_form.html',context)

def product_overview(request,id):

    product = Product.objects.get(id=id)
    more = Product.objects.filter(
            category=product.category
        ).exclude(id=id)[:5]  # Limit results for efficiency
    rating=[]
    for i in range(6-product.product_rating):
        rating.append(True)
    for i in range(product.product_rating-1):
        rating.append(False)
    
    if product.stock ==0:
        date = Ordered.objects.filter(product=product).last()
        purchased = date.orderedby.date
    else:
        purchased = 0
        
    context = {
        'product' : product,
        'image_details' : more,
        'rating' : rating,
        'purchased' : purchased
    }

    return render(request,'overview.html',context)

@login_required(login_url='/login')
def add_to_group(request, table_name, id):
    # Map table name to the correct model
    model_mapping = {
        'favorite': Favorite,
        'cart': Cart,
    }
    model = model_mapping.get(table_name.lower())

    if not model:
        return HttpResponse("Invalid table name", status=400)

    # Fetch the product
    product = Product.objects.get(id=id)

    # Check if product is sold
    if product.stock==0:
        messages.warning(request, "This product is already sold.")
        return redirect('home')  # Replace 'home' with the appropriate page name

    # Check if the product is already in the model (e.g., cart or favorite)
    existing_item = model.objects.filter(product_id=product.id, user=request.user).first()

    if existing_item:
        # Increment quantity if in cart
        if table_name.lower() == 'cart':
            if existing_item.quantity >= existing_item.product.stock:
                messages.warning(request, "Product Stock Limited")
            else:
                existing_item.quantity += 1
                existing_item.save()
                messages.success(request, "Product quantity updated in your cart.")
    else:
        # Create new entry
        if table_name.lower() == 'cart':
            if product.stock <= 0:
                messages.warning(request, "Product Stock Limited")
            else:
                model.objects.create(product_id=product.id, quantity=1, user=request.user)
                messages.success(request, "Product added to your cart.")
        elif table_name.lower() == 'favorite':
            model.objects.create(product_id=product.id, user=request.user)
            messages.success(request, "Product added to your favorites.")

    return redirect('/')

def update_quantity(request,cart_id):
    if request.method=="POST":
        cart = Cart.objects.filter(id = cart_id)
        quantity = request.POST.get('quantity')
        cart.update(quantity = quantity)
        return redirect('/cart')

    return HttpResponseRedirect(request.path)

@login_required(login_url='/login')
def cart_page(request):
    cart_products_id = Cart.objects.filter(user=request.user)
    total_price = sum(item.quantity * item.product.product_price for item in cart_products_id)
    context = {
        'cart_products' : cart_products_id,
        'total_price' : total_price
    }
    return render(request,'cart_page.html',context)
    # return HttpResponse(cart_products[0].product_price)

def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        cart_item = Cart.objects.get(product_id=product_id, user=request.user)
        cart_item.quantity = quantity
        cart_item.save()
        return redirect('/cart')
    return redirect('/home')

def remove_from_group(request, table_name, id):
    model_mapping = {
        'favorite': Favorite,
        'cart': Cart,
    }
    
    model = model_mapping.get(table_name.lower())

    if model:
        # Get the object and delete it
        obj = get_object_or_404(model, user=request.user,product_id = id)
        obj.delete()
        if table_name == 'favorite':
            rtn = "fav_page"
        else:
            rtn = "cart"
        return redirect("/"+ rtn)  # Redirect to the appropriate page
    else:
        return HttpResponse("Invalid table name", status=400)


@login_required(login_url='/login')
def fav_page(request):
    fav_products_id = Favorite.objects.filter(user=request.user)
    product_id = [x.product_id for x in fav_products_id]
    fav_products = Product.objects.filter(id__in=product_id)
    context = {
        'fav_products' : fav_products,
    }
    return render(request,'fav_page.html',context)

import time
def checkout_page(request,id=0):
    result = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()
    if request.method=="POST":
        payment_method  = request.POST.get('method')
        if payment_method == 'esewa':
            messages.error(request, f"Error during payment:")
            return HttpResponseRedirect(request.path)
            # try:
            #     cart_objects = Cart.objects.filter(user=request.user)
            #     OrderedBy.objects.create(
            #         userprofile = UserProfile.objects.get(user=request.user),
            #         address = request.POST.get('address', 'banepa'),
            #         total = sum(item.product.product_price * item.quantity for item in cart_objects)
            #     )
            #     for x in cart_objects:
            #         Ordered.objects.create(
            #             product = x.product,
            #             quantity = x.quantity,
            #             orderedby = OrderedBy.objects.last()
            #         )
            #         product = Product.objects.filter(id=x.product.id)
            #         if product[0].stock - x.quantity >= 0:
            #             product.update(stock = product[0].stock - x.quantity)
            #         else:
            #             messages.error(request, "Insufficient stock for product: " + product[0].product_name)
            #             return HttpResponseRedirect(request.path)
            # except Exception as e:
            #     messages.error(request, f"Error during payment: {e}")
            #     return HttpResponseRedirect(request.path)
            # try:
            #     return HttpResponseRedirect(f"esewarequest.html?o_id={OrderedBy.objects.last().id}")
            # except Exception as e:
            #     messages.error(request, f"Error during payment: {e}")
            #     return HttpResponseRedirect(request.path)

        elif payment_method == 'codt':
            cart_objects = Cart.objects.filter(user=request.user)

            try:
                user_profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                # Handle the case where no UserProfile exists
                user_profile = UserProfile.objects.create(user=request.user, phone="Unknown", address="Unknown")
            
            if request.POST.get('address'):
                address = request.POST.get('address')
            else:
                address = user_profile.address
            OrderedBy.objects.create(
                userprofile = UserProfile.objects.get(user=request.user),
                address = address,
                total = sum(item.product.product_price * item.quantity for item in cart_objects)
            )
            for x in cart_objects:
                Ordered.objects.create(
                    product = x.product,
                    quantity = x.quantity,
                    orderedby = OrderedBy.objects.last(),
                )
                product = Product.objects.filter(id=x.product.id)
                product.update(stock = product[0].stock - x.quantity)

            Cart.objects.all().delete()
            return redirect('/')
        elif payment_method == 'codf':
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                if request.POST.get('address'):
                    address = request.POST.get('address')
                else:
                    address = user_profile.address

                quantity = int(request.POST.get('quantity'))
                product = Product.objects.filter(id=request.POST.get('product_id'))
                
                OrderedBy.objects.create(
                    userprofile = UserProfile.objects.get(user=request.user),
                    address = address,
                    total = quantity*product[0].product_price
                )
            
                Ordered.objects.create(
                    product = product[0],
                    quantity = quantity,
                    orderedby = OrderedBy.objects.last()
                )
            except Exception as e:
                messages.error(request, f"Error during payment: {e}")
                return HttpResponseRedirect(request.path)
            
            product.update(stock = product[0].stock - quantity)
            return redirect('/')
            
    result = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()
    if id==0:
        cart_products = Cart.objects.filter(user=request.user)
        total_price = sum(item.quantity * item.product.product_price for item in cart_products)
        cart='codt'
    else:
        cart_products = Product.objects.filter(id=id)
        total_price = cart_products[0].product_price
        cart='codf'
    
    address = UserProfile.objects.get(user=request.user).address
    context = {
        'cart_products' : cart_products,
        'total_price' : total_price,
        'cart': cart,
        'signature' : result,
        'address' : address
    }
    return render(request,'checkout_page.html',context)


def verify_payment(request):
    if request.method == 'POST':
        try:
            # Extract the necessary parameters from the response
            status = request.POST.get('status')
            amount = request.POST.get('amt')
            transaction_id = request.POST.get('pid')  # Payment ID (or transaction ID)
            checksum = request.POST.get('checksum')

            # Prepare the data for checksum validation
            data = f"amt={amount}&pid={transaction_id}&scd={settings.ESEWA_MERCHANT_ID}&status={status}"
            calculated_checksum = hashlib.md5(data.encode('utf-8')).hexdigest()

            # Compare checksum
            if calculated_checksum == checksum:
                # Verify payment success
                if status == 'Success':
                    # Update the transaction status to completed
                    transaction = EsewaTransaction.objects.get(id=transaction_id)
                    transaction.status = 'completed'
                    transaction.save()
                    return JsonResponse({"message": "Payment Successful", "status": "success"})
                else:
                    return JsonResponse({"message": "Payment Failed", "status": "failed"})
            else:
                return JsonResponse({"message": "Checksum Mismatch", "status": "error"})
        except Exception as e:
            print(f"Error during payment verification: {e}")
            return JsonResponse({"message": "Invalid Request", "status": "error"})
    return JsonResponse({"message": "Invalid Request", "status": "error"})

def send_email(request):
    send_email_to_clint()
    return redirect('/')

@login_required(login_url='/login')
def order_page(request):
    if request.method=="POST":
        id = request.POST.get('id')
        orderby = get_object_or_404(OrderedBy, id=id, userprofile=UserProfile.objects.get(user=request.user))

        for x in Ordered.objects.filter(orderedby=orderby):
            product = Product.objects.filter(id=x.product.id)
            product.update(stock = product[0].stock + x.quantity)
        orderby.delete()
        return HttpResponseRedirect(request.path)

    ordersby = OrderedBy.objects.filter(userprofile=UserProfile.objects.get(user=request.user))
    orders = Ordered.objects.filter(orderedby__in=ordersby)
    context = {
        'ordersby' : ordersby,  
        'orders' : orders
    }
    return render(request,'order_page.html',context)

def vendor_page(request):
    my_products = Product.objects.filter(created_by=request.user).count()
    p = Product.objects.filter(created_by=request.user)
    ordered = Ordered.objects.filter(product__in=p)
    total_sales = Ordered.objects.filter(product__in=p, orderedby__process=True).count()
    if total_sales == 0:
        total_sales = 0
    context = {
        'my_products' : my_products,
        'total_sales' : total_sales
    }
    return render(request,'vendor/vendor.html',context)

def edit_product(request,id):
    if request.method == 'POST':
        try:
            data = request.POST
            print('rocket',data.get('categories'))
            product = Product.objects.get(id=data.get('product_id'))    
            product.product_name = data.get('product_name') 
            product.product_description = data.get('product_description')
            product.product_price = data.get('product_price')
            product.product_rating = int(data.get('cond'))
            product.category = Category.objects.get(category_name__icontains = data.get('categories'))
            product.save()
            messages.success(request, "Product updated successfully.")
            return HttpResponseRedirect(request.path)
        except Exception as e:
            messages.error(request, f"Error updating product: {e}")
            return HttpResponseRedirect(request.path)

    product = Product.objects.get(id=id)
    product_images = ProductImage.objects.filter(product=product).first()
    context = {
        'product' : product,
        'product_images' : product_images,
        'categories' : Category.objects.all()
    }
    return render(request,'vendor/update_product.html',context)

def delete_product(request,id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('/')

# try:
#             except Exception as e:
#                 messages.error(request, f"Error during payment: {e}")
#                 return HttpResponseRedirect(request.path)