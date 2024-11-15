<h1> Django </h1>
<hr>
<a href="#authentication">Django Authentications</a>
<hr>

<div id="authentication" class="authentication">
    <h2>Django Authentication</h2>
    <hr>
    <a href="#register">Register</a>
    <a href="#login">Login</a>
    <hr>
        <div id = 'register'>
            <section id='register.html'>
                <h2>In models.py</h2>
            <section>           
                from django.contrib.auth.models import User
                class Rushal(models.Model):
                    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True,blank=True)
            </section>
            </section>
                <h2>In Register.html</h2>
                <p>from  register.html we can take the form as method post and enctype="multi..."</p>
            </section>
            <section id ='register.views'>
                <h2>In Views.py</h2>
                <pre>

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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
