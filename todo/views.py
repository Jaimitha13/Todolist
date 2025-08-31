from django . shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from todo import models
from todo.models import Todo
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.decorators import login_required
def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        
        if User.objects.filter(username=fnm).exists():
          return render(request,'signup.html',{
              'error':'Username already exists',
              'fnm':fnm,
              'email':email
          }) 

        if User.objects.filter(email=email).exists():
          return render(request,'signup.html',{
              'error':'email id already exists',
              'fnm':fnm,
              'email':email
          })  

       
        my_user = User.objects.create_user(username=fnm, email=email, password=pwd)
        my_user.save()


        user = authenticate(request, username=fnm, password=pwd)
        if user is not None:
            auth_login(request, user)
            return redirect('/todolist')   

        return redirect('/login') 

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        try:
           user_exist = User.objects.get(username=fnm)

        except User.DoesNotExist:
            return render(request,'login.html',{
                'error':'No account existed with this username',
                'fnm':fnm})
            
        user = authenticate(request, username=fnm, password=pwd)
        if user is not None:
            auth_login(request, user)
            return redirect('/todolist')
        else:
            
            return render(request, 'login.html', {
                'error': 'Your username or password is incorrect',
                'fnm': fnm})
    return render(request, 'login.html')

@login_required(login_url='/login')
def todolist(request):
    if request.method=='POST':
       title = request.POST.get('title')
       print(title)
       obj=models.Todo(title=title,user=request.user)
       obj.save()
       res=models.Todo.objects.filter(user=request.user).order_by('-date')
       return redirect('/todolist',{'res':res})
    res=models.Todo.objects.filter(user=request.user).order_by('-date')
    return render(request,'todolist.html',{'res':res})

@login_required(login_url='/login')
def edit(request, srno):
    obj = get_object_or_404(models.Todo, srno=srno)

    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            obj.title = title
            obj.save()
        
        return redirect('/todolist/')

  
    return render(request, 'edit.html', {'obj': obj})
      

@login_required(login_url='/login')
def delete(request,srno):

    obj=models.Todo.objects.get(srno=srno)
    obj.delete()
    return redirect('/todolist/')

def signout(request):
    logout(request)
    return redirect('/login/')