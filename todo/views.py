from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
def home(request,n):
    if request.user.is_authenticated:    
        if request.method=='POST':
            t=request.POST.get('title')
            d=request.POST.get('desc')
            todos.objects.create(title=t,desc=d,user=n)
            return redirect(f'/home/{n}')
        q=todos.objects.filter(user=n)
        context={"todos":q} 
        if request.GET.get('search'):
            s=request.GET.get('search')  
            qq=todos.objects.filter(user=n)
            r=qq.filter(title__icontains=s)
            contex={"todos":r}
            return render(request,'home.html',contex)           
        return render(request,'home.html',context)
    else:
        return redirect('/')

def delete(request,n,id):
    q=todos.objects.filter(user=n)
    q.get(id=id).delete()
    return redirect(f'/home/{n}')

def update(request,n,id):
    if request.method=='POST':
        t=request.POST.get('title')
        d=request.POST.get('desc')
        q=todos.objects.filter(user=n)
        u=q.get(id=id)
        u.title=t
        u.desc=d
        u.save()
        return redirect(f'/home/{n}')
    tt=todos.objects.get(id=id)
    context={"title":tt.title,"desc":tt.desc}  
    return render(request,'update.html',context)

def login_page(request):
    if request.method=='POST':
        n=request.POST.get('name')
        p=request.POST.get('pass')
        user=authenticate(username=n,password=p)
        if user is not None:
            login(request,user)
            messages.success(request,'Logedin successfully.')
            return redirect(f'/home/{n}')
        else:
            messages.info(request,'Invalid credentials.')
            return redirect('/login')

    return render(request,'login.html')

def signin_page(request):
    if request.method=='POST':
        n=request.POST.get('name')
        e=request.POST.get('email')
        p=request.POST.get('pass')
        cp=request.POST.get('cpass')

        if p!=cp:
            messages.info(request,'password does not match')
            return redirect('/')
            
        elif User.objects.filter(username=n).exists():
            messages.info(request,'Username already taken')
            return redirect('/')
        
        elif User.objects.filter(email=e).exists():
            messages.info(request,'Email already taken')
            return redirect('/')
        
        else:
            user=User.objects.create_user(username=n,email=e,password=p)
            user.save()
            login(request,user)
            messages.success(request,'Account created successfully.')
            return redirect(f'/home/{n}')
    return render(request,'signin.html')

def logout_page(request):
    logout(request)
    messages.success(request,'Loged out successfully.')
    return redirect('/login')


# @csrf_exempt
# def check(requesdvvat):
#     if request.is_ajax():
#         message = "Yes, AJAX!"
#     else:
#         message = "Not Ajax"
#     return HttpResponse(message)
