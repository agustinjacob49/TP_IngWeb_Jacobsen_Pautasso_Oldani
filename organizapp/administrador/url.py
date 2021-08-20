from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('login/', login, name="login"),
]