from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages 

def index(request):
    return render(request, 'login_reg/index.html')

def register(request):
    #REMEMBER THAT ORDER MATTERS!
    response = User.objects.register(
        request.POST['name'],
        request.POST['username'],
        request.POST['password'],
        request.POST['confirm'],
        request.POST['date_hired'],
    )
    # the below response is from the RETURN response from THE MODELS.py
    if response['valid']:
        #make session variable to keep track of user
        request.session['user_id'] = User.objects.get(username = request.POST['username']).id
        request.session['user_name'] = User.objects.get(username = request.POST['username']).username
        request.session['name'] = User.objects.get(username = request.POST['username']).name
        messages.add_message(request, messages.INFO, "You have successfully logged in!")
        return redirect('/dashboard')
    else:
        for error_message in response['errors']:
            # add messages one at a time and say that they are error messages IN THE messages variable
            messages.add_message(request, messages.ERROR, error_message)
        return redirect('/')

def login(request):
     #REMEMBER THAT ORDER MATTERS!
    response = User.objects.login(
        request.POST['username'],
        request.POST['password'],
    )
    if response['valid']:
        #make session variable to keep track of user
        request.session['user_id'] = User.objects.get(username = request.POST['username']).id
        request.session['user_name'] = User.objects.get(username = request.POST['username']).username
        request.session['name'] = User.objects.get(username = request.POST['username']).name
        messages.add_message(request, messages.INFO, "You have successfully logged in!")
        return redirect('/dashboard')
    else:
        for error_message in response['errors']:
            # add messages one at a time and say that they are error messages IN THE messages variable
            messages.add_message(request, messages.ERROR, error_message)
        return redirect('/')

def logout(request):
    request.session.clear()
    messages.add_message(request, messages.INFO, "You've been logged out!")
    return redirect('/')

# Create your views here.
