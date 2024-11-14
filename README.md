<h1> Django </h1>
<a href="#authentication">Django Authentications</a>

<div id="authentication" class="authentication">
    <h2>Django Authentication</h2>
    <a href="#register">Register</a>
    <hr>
        <div id = 'register'>
            <hr>
            <a href="#register.views">Register</a><a href="#register.views">Register</a>
            <hr>
            <section id='register.html'>
                <h2>Register.html</h2>
                <p>from  register.html we can take the form as method post and enctype="multi..."</p>
            </section>
            <section id ='register.views'>
                <h2>to get the proper values </h2>
                <pre>
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
                </pre>
            </section>
        </div>
</div>
