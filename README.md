<h1> Django </h1>
<a href="#authentication">Django Authentications</a>

<section id="authentication" class="authentication">
    <h2>Django Authentication</h2>
    <a href="#register">Register</a>
    <hr>
    <div>
        <section id = 'register'>
            <h2>Register.html</h2>
            <pre>
                {% extends "base.html" %}
{% block start%}

<div class="container mt-5">
    <form class="col-6 mx-auto card p-3 shadow-lg" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <h2 style="text-align: center;">REGISTER</h2>
        <hr>
        
        {% if messages %}
        <div class="alert alert-primary" role="alert">
            {% for message in messages %}
            {{message}}
            {% endfor %}
        </div>
        {% endif %}


        <div class="mb-3">
            <label for="exampleInputEmail1" class="form-label">First Name</label>
            <input type="text" class="form-control" name= "first name"id="exampleInputEmail1" aria-describedby="emailHelp">
        </div>

        <div class="mb-3">
            <label for="exampleInputEmail1" class="form-label">Last Name</label>
            <input type="text" class="form-control" name= "last name"id="exampleInputEmail1" aria-describedby="emailHelp">
        </div>

        <div class="mb-3">
          <label for="exampleInputEmail1" class="form-label">User Name</label>
          <input type="text" class="form-control" name="username" id="exampleInputEmail1" aria-describedby="emailHelp">
          <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
        </div>

        <div class="mb-3">
          <label for="exampleInputPassword1" class="form-label">Password</label>
          <input type="password" class="form-control" name="password" id="exampleInputPassword1">
        </div>
        <div>
            <a href="/login/">Login</a> directly if already have an account
            <hr>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>

      </form>
</div>
{% endblock %}
            </pre>
        </section>
    </div>
    <pre>
        {% if messages %}
        <div class="alert alert-primary" role="alert">
            {% for message in messages %}
            {{message}}
            {% endfor %}
        </div>
        {% endif %}
        
    </pre>
</section>
