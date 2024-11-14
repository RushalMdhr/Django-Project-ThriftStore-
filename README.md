<h1> Django </h1>
<a href="#project">About</a>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<section id="project" class="project">
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
