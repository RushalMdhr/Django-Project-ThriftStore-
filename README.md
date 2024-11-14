<h1> Django </h1>
<p>
def register_page(request):
    if request.method=="POST":
        first_name = request.POST.get('first name')
        last_name = request.POST.get('last name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request, "username already exists")
            return redirect('/register/')
            

        user = User.objects.create(
            first_name = first_name ,
            last_name = last_name ,
            username = username ,
        )

        user.set_password(password)
        user.save()
        messages.info(request, "Account created sucessfully")


    return render(request,'register.html')
    </p>
