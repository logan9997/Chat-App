from django.urls import path
from .views import (
    home, login, logout
)

urlpatterns = [
    path('', home.home, name='home'),
    path('login/', login.login, name='login'),
    path('logout/', logout.logout, name='logout')
]