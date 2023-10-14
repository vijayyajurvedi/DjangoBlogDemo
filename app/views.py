from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from app.models import Blogs, Contact

# Below Imports are done for sending emails
from django.conf import settings
from django.core.mail import send_mail
from django.core  import mail

from django.core.mail.message import EmailMessage

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')



def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")

        mycontact = Contact.objects.create(
            name=name, email=email, phone=phone, description=desc)
        mycontact.save()

        # from_email=settings.EMAIL_HOST_USER
        # connection=mail.get_connection()
        # connection.open()
        # email_message=mail.EmailMessage(f'Email from {name}',f'UserEmail: {email}\nUserPhone :{phone}\n\n\n Query:{desc}',from_email,['vijay.yajurvedi@gmail.com','gururaj.yajurvedi@gmail.com'],connection=connection)
        # connection.send_messages([email_message])
        # connection.close()

        messages.success(request,"Thanks For Reaching Us , we will reach to you soon")
        return redirect('/contact')

    return render(request, 'contact.html')


def handlelogout(request):
    logout(request)
    messages.info(request, "Logout Success")
    return redirect('/login')


def handlelogin(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("pass1")

        myuser = authenticate(username=uname, password=password)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Sucessfull")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
            return redirect("/login")
    return render(request, 'login.html')


def handlesignup(request):

    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("pass1")
        confirmpassword = request.POST.get("pass2")
        # print(uname,email,password,confirmpassword)
        if password != confirmpassword:
            messages.warning(
                request, "Password & Confirm Password Should Match")
            return redirect('/signup')

        try:
            if User.objects.get(username=uname):
                messages.info(request, "Username is already taken")
                return redirect('/signup')
        except:
            pass

        try:
            if User.objects.get(email=email):
                messages.info(request, "Email is already taken")
                return redirect('/signup')
        except:
            pass

        myuser = User.objects.create_user(uname, email, password)
        myuser.save()
        messages.success(request, "Sign-up Sucessfull")
        return redirect('/signup')
    return render(request, 'signup.html')

def handleBlog(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Hey Just Login and Use My Website")
        return redirect('/login')
     
    allPosts = Blogs.objects.all()
    context={'allPosts':allPosts}
    return render(request,'blog.html',context=context)

def search(request):
    query=request.GET['search']
    if len(query)>100:
        allPosts=Blogs.objects.none()
    else:
        allPostsTitle=Blogs.objects.filter(title__icontains=query)
        allPostsDesc=Blogs.objects.filter(description__icontains=query)
        allPosts= allPostsTitle.union(allPostsDesc)
    if allPosts.count()==0:
        messages.warning(request,"No Search Result")

    params={'allPosts':allPosts,'query':query}

    return render(request,'search.html',params)