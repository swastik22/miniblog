from django.shortcuts import render, HttpResponseRedirect
from .forms import SignupForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group

# Home views.
def home(request):
    posts=Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})

# About Views.
def about(request):
    return render(request,'blog/about.html')

# Contact Views.
def contact(request):
    return render(request,'blog/contact.html')

# Dashboard Views.
def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user = request.user
        full_name=user.get_full_name()
        gps=user.groups.all()

        return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name,'gps':gps})
    else:
        return HttpResponseRedirect('/login/')

# Logout Views.
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Signup Views.
def user_signup(request):
    if request.method=='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            messages.success(request,"Great !! You are an author now.")
            user= form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignupForm() 
    return render(request,'blog/signup.html',{'form':form})

# Login Views.
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass= form.cleaned_data['password']
                user= authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"You are login !!")
                    return HttpResponseRedirect('/dashboard/')
        else:            
            form = LoginForm()
        return render(request,'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')   

# ADD POST
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form= PostForm(request.POST)
            if form.is_valid():
                form.save()
                form=PostForm()
        else:
            form=PostForm()
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

# Update POST
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form=PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form =PostForm(instance=pi)        
        return render(request,'blog/updatepost.html' , {'form':form})
    else:
        return HttpResponseRedirect('/login/')
# Delete post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')