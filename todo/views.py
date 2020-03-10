from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .forms import TodoForm
from .models import Todo
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', { 'form' : UserCreationForm() } )
    else:
        # Creating new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                context = { 
                    'form' : UserCreationForm(),
                    'error' : "Username Already exist",
                }
                return render(request, 'todo/signupuser.html', context)

        else:
            # user didnt enter password same in both field
            context = { 
                'form' : UserCreationForm(),
                'error' : "Password didnt match",
            }
            return render(request, 'todo/signupuser.html', context)

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', { 'form' : AuthenticationForm() } )
    else:
        # Login user
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', { 'form' : AuthenticationForm(), 'error' : 'username and password does not match' } )
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'todo/home.html')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', { 'form' : TodoForm() })
    else:
        try:
            todo = TodoForm(request.POST)
            new_todo = todo.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', { 'form' : TodoForm(), 'error': 'Bad Value Pass in. Try agian' })

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos' : todos}) 

@login_required
def viewtodo(request, todo_pk):
    # Retrivie the todos of login user
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'form':form, 'todo' : todo})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except:
            return render(request, 'todo/viewtodo.html', { 'form' : TodoForm(), 'error': 'Bad Value Pass in. Try agian','todo':todo })

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos': todos})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')