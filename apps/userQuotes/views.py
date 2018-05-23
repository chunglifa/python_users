from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
import bcrypt

# LOGIN AND REGISTRATION
def index(request):
    print('RENDERING INDEX HTML')
    return render(request, "userQuotes/index.html")

def registration(request):
    if request.method == 'POST':
        request.session.clear()
        errors = User.objects.registration_validator(request.POST)
        print(errors)
        if len(errors):
            for key, value in errors.items():
                messages.error(request,value)
            return redirect("/")
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            newUser = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], pw_hash = hashed_pw)
            messages.success(request, 'Successfully registered!')
            request.session['id'] = newUser.id
            return redirect("/welcome")

def login(request):
    print('LOGIN INITIATING')
    if request.method == 'POST':
        request.session.clear()
        errors = User.objects.login_validator(request.POST)
        print(errors)
        if len(errors):
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            request.session['id'] = User.objects.get(email = request.POST['email']).id
            print(request.session['id'])
            messages.success(request, 'Successfully logged in!')
            return redirect('/welcome')

# RENDERING OTHER HTML LANDING PAGES

def welcome(request):
    print('RENDER WELCOME PAGE')
    user = User.objects.get(id = request.session['id'])
    quotes = Quote.objects.all()
    print(user)
    context ={
        'user': user,
        'quotes': quotes
    }
    return render(request, "userQuotes/welcome.html", context)

def user(request, id):
    print('RENDER USER PROFILE')
    user = User.objects.get(id = id)
    quotes = User.objects.get(id=id).uploaded_quotes.all()
    context ={
        'user': user,
        'quotes': quotes
    }
    return render(request, "userQuotes/user.html",context)

def edit(request, id):
    print('EDIT FORM')
    user = User.objects.get(id = id)
    context ={
        'user': user
    }
    return render(request, "userQuotes/edit.html",context)

def logout(request):
    print('LOGOUT')
    request.session.clear()
    return redirect('/')

# PROCESSING METHODS:

def add_quote(request):
    print(request.POST)
    user = User.objects.get(id = request.session['id'])
    if request.method == 'POST':
        errors = Quote.objects.book_validator(request.POST)
        print(errors)
        if len(errors):
            for key, value in errors.items():
                messages.error(request,value)
            return redirect("/welcome/")
        else:
            newQuote = Quote.objects.create( content = request.POST['quote'], author = request.POST['author'], uploader = User.objects.get(id=request.session['id']))
            print('UPLOAD SUCCESSFUL')
    return redirect("/welcome")

def like(request):
    print(request.POST)
    user = User.objects.get(id = request.session['id'])
    quote = Quote.objects.get(id = request.POST['quote_id'])
    if request.method == 'POST':
        errors = Like.objects.review_validator(request.POST)
        print(errors)
        if len(errors):
            for key, value in errors.items():
                messages.error(request,value)
        if User.objects.get(id = request.session['id']).likes.filter(quote_id = request.POST['quote_id']):
            return redirect("/welcome/")
        else:
            newLike = Like.objects.create( user = user, quote = quote)
            print('NEW LIKE CREATED!')
    return redirect("/welcome")

def update(request):
    print('UPDATE METHOD TO PROCESS')
    if request.method == 'POST':
        id = request.POST['id']
        errors = User.objects.update_validator(request.POST)
        print(errors)
        if len(errors):
            for key, value in errors.items():
                messages.error(request,value)
            return redirect("/welcome")
        else:
            editUser = User.objects.get(id=id)
            editUser.first_name = request.POST['first_name']
            editUser.last_name = request.POST['last_name']
            editUser.email = request.POST['email']
            editUser.save()
            return redirect("/welcome")
def delete(request,id):
    print('DESTROY METHOD - PROCESS')
    Quote.objects.get(id = id).delete()
    return redirect("/welcome")

from django.shortcuts import render

# Create your views here.
