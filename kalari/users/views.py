from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
import random
from django.core.mail import send_mail
from django.conf import settings
def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')



def Sregister(request):
    if request.method == "POST":
        form = userRegister(request.POST,request.FILES)
        if form.is_valid():
            username = form.cleaned_data['name']
            if User.objects.filter(username = username).exists():
                messages.error(request, 'name/username  already exists')
                return render(request, 'sregister.html')
            email = form.cleaned_data['email']
            if User.objects.filter(email = email).exists():
                messages.error(request, 'Email already exists')
                return render(request, 'sregister.html')
            
            password = form.cleaned_data['password']
            password = make_password(password)
            user = form.save(commit = False)
            user.username = username
            user.role = "student"
            user.password = password
            user.save()
            messages.success(request, 'Registration successful')
            return redirect('login')
        else:
            print(form.errors)
            messages.error(request,form.errors)
    form = userRegister()
    return render(request, 'sregister.html',{'form':form})




def Tregister(request):
    if request.method == "POST":
        form = tregister(request.POST,request.FILES)
        if form.is_valid():
            username = form.cleaned_data['name']
            if User.objects.filter(username = username).exists():
                messages.error(request, 'name/username  already exists')
                return render(request, 'tregister.html')
            email = form.cleaned_data['email']
            if User.objects.filter(email = email).exists():
                messages.error(request, 'Email already exists')
                return render(request, 'tregister.html')
            
            password = form.cleaned_data['password']
            password = make_password(password)
            user = form.save(commit = False)
            user.username = username
            user.role = "teacher"
            user.password = password
            user.save()
            messages.success(request, 'Registration successful')
            return redirect('login')
        else:
            print(form.errors)
            messages.error(request,form.errors)
    form = tregister()
    return render(request, 'tregister.html',{'form':form})






def loginall(request):
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request,"login success")
                return redirect('/homepage')
            else:
                messages.error(request, 'User is deactivated')
                return render(request, 'login.html')
        else:
            messages.error(request, 'invalid username or password')
            return render(request, 'login.html')

    return render(request, 'login.html')

def logoutall(request):
    logout(request)
    return redirect('/')

def homepage(request):
    return render(request,'homepage.html')




def view_instructors(request):
    instructors = User.objects.filter(role='teacher')
    return render(request, "view_instructor.html", {"instructors": instructors})

def view_students(request):
    students = User.objects.filter(role='student')
    return render(request, "view_students.html", {"students": students})


def activate(request,id):
    user = User.objects.get(id = id)
    user.is_active = True
    user.save()
    return redirect('homepage')
def deactivate(request,id):
    user = User.objects.get(id = id)
    user.is_active = False
    user.save()
    return redirect('homepage')





def forgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if User.objects.filter(email = email).exists():
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            send_mail(
                 subject = "one time password",
                 message = f"Your one time otp is {otp}",
                 from_email = settings.EMAIL_HOST_USER,
                 recipient_list = [email],
                 fail_silently = True
                 
             )
            user = User.objects.get(email = email)
            user.password  = make_password(otp)
            user.save()
            return redirect('login')
      
    
    return render(request,'forgotPassword.html')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST.get('confirm')
        user = User.objects.get(id = request.user.id)
        user.password  = make_password(password)
        user.save()
        logout(request)
        return redirect('login')
    return render(request,'resetPassword.html')


def editProfile(request):
    return render(request,'editProfile.html')

def changeUsername(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        user = request.user
        user.username  = name
        user.save()
        return redirect('/editProfile')
    return render(request,'changeUsername.html')


def changeProfile(request):
    if request.method == 'POST':
        name = request.FILES.get('img')
        user = request.user
        user.image  = name
        user.save()
        return redirect('/editProfile')
    return render(request,'changeImage.html')