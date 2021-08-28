from django.urls import path
from . import views
urlpatterns = [
    path('', views.signup),
    path('signup', views.signup),
    path('home', views.index),
    path('login', views.login),
    path('logout', views.logout)

]
