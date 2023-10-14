
from app import views
from django.urls import include, path

urlpatterns = [

    path('', views.index,name='index'),
    path('about', views.about,name='about'),
    path('contact', views.contact,name='contact'),
    path('blog', views.handleBlog,name='handleBlog'),

    path('search', views.search,name='search'),


    path('login', views.handlelogin,name='handlelogin'),
    path('logout', views.handlelogout,name='handlelogout'),

    path('signup', views.handlesignup,name='handlesignup'),


]
