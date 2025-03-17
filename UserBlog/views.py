from lib2to3.fixes.fix_input import context

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import CreateBlog, CreateBlog, CreatePost
from .models import *


# --------------------------------DASHBOARD--------------------------------------------
login_required(login_url='login/')
def dashboard(request):
    blogs = Blog.objects.all()

    context = {
        'blogs':blogs
    }
    return render(request, 'dashboard.html', context )


login_required(login_url='login/')
def blog(request, blog_id):
    blogs = Blog.objects.get(id = blog_id)
    posts = Post.objects.filter(blog = blogs)
    return render(request, 'blog.html', {'blog':blogs, 'posts':posts})


login_required(login_url='login/')
def myblogs(request):
    blogs = Blog.objects.filter(created_by = request.user)
    return render(request, 'myblogs.html', {'blogs':blogs})



# ------------------------------AUTH----------------------------------------------------

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirm_password =  request.POST.get('confirm_password')
        prof_pic = request.POST.get('prof_pic')
        bio = request.POST.get('bio')

        if password != confirm_password:
            messages.error(request, "Password doesn't match. Please try again ")
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')

        user = User.objects.create(username=username, email=email, password=password)
        profile = Profile.objects.create(user=user, bio=bio)
        login(request, user)
        messages.success(request, 'Signed up successfully!')
        return redirect('dashboard')
    return render(request, 'signup.html' )

def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        email_user = User.objects.filter(email=email).first()
        if email_user:
            user = authenticate(request, username=email_user.username, password=password)
        else:
            user = None

        if user:
            login(request, user)
            messages.success(request, 'Signed in successfully!')
            return redirect(request.GET.get('next', 'dashboard'))
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('signin')

    return render(request, 'signin.html')

login_required(login_url='login/')
def signout(request):
    logout(request)
    return redirect('signin')

# ----------------------------------BLOGS-------------------------------------

login_required(login_url='login/')
def create_blog(request):
    if request.method == 'POST':
        form = CreateBlog(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.created_by = request.user
            blog.save()
            return redirect('blog', blog_id = blog.id)
    else:
        form = CreateBlog()

    return render(request, 'create_blog.html', {'form':form, 'button_text':'Create'})


login_required(login_url='login/')
def create_post(request, blog_id):
    print("Received blog_id:", blog_id)
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        form = CreatePost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.blog = blog
            post.save()

            return redirect('blog', blog_id = blog.id)
    else:
        form = CreatePost()

    return render(request, 'create_post.html', {'form':form})

@login_required(login_url='login/')
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, created_by = request.user)

    if request.method == 'POST':
        form = CreateBlog(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('myblogs')
    else:
            form = CreateBlog(instance=blog)

    return render(request, 'create_blog.html', {'form':form, 'button_text': "Save"})


@login_required(login_url='login/')
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id = blog_id, created_by = request.user)
    if request.method == "POST":
        blog.delete()
        return redirect('myblogs')
    return render(request, 'confirm_delete.html', {'blog': blog})

@login_required(login_url='login/')
def edit_post(request, post_id):
     post = get_object_or_404(Post, id = post_id)
     if request.method == 'POST':
         form = CreatePost(instance=post)
         if form.is_valid():
             form.save()
         return redirect('myblogs')
     else:
         form = CreatePost(instance=post)

     return render(request, 'create_post.html', {'form':form})

@login_required(login_url='login/')
def delete_post(request, post_id):
    post  = get_object_or_404(Post, id = post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('myblogs')
    return render(request, 'confirm_delete_post.html', {'post':post})


@login_required(login_url='login/')
def read_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    return render(request, 'read_post.html', {'post':post})

@login_required(login_url='login/')
def my_profile(request):
    profile = get_object_or_404(Profile, user = request.user)
    return render(request, 'my_profile.html', {'profile':profile})

