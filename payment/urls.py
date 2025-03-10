from django.urls import path
from .views import *

urlpatterns = [
    path("esewa-request/", EsewaRequestView.as_view(), name="esewarequest"),    
]