from django.shortcuts import render , HttpResponseRedirect
from .forms import SignUpForm , LoginForm , PostForm
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group

# Create your views here.

#home
def home(request):
    post = Post.objects.all()
    return render(request,'blogg/home.html',{"post":post})
#about
def about(request):
    return render(request,'blogg/about.html')
#contact
def contact(request):
    return render(request,'blogg/contact.html')

#signupform
def user_signup(request):
    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request,'blogg/signup.html',{"form":form})

#loginform

def user_login(request):
    if request.method=="POST":
        form = LoginForm(request=request , data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/dashboard/') 
    else:
        form = LoginForm()
    return render(request,'blogg/login.html',{"form":form})

#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#dashboard
def dashboard(request):
    post = Post.objects.all()
    user = request.user
    full_name = user.get_full_name()
    gps = user.groups.all()
    return render(request,'blogg/dashboard.html',{"post":post,"full_name":full_name,"group":gps})

# add new post

def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        form = PostForm()
    return render(request,'blogg/add_post.html',{"form":form})

# update post 

def update_post(request,id):
    if request.method=="POST":
        pi = Post.objects.get(pk=id)
        form = PostForm(request.POST , instance=pi)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        pi = Post.objects.get(pk=id)
        form = PostForm(instance=pi)
    return render(request,'blogg/update_post.html',{"form":form})

# delete post 

def delete_post(request,id):
    if request.method=="POST":
        pi = Post.objects.get(pk=id)
        pi.delete()
    return HttpResponseRedirect('/dashboard/')
