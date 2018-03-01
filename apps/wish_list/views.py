from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import List, User
from datetime import datetime
from django.contrib import messages

def dashboard(request):
    if not 'user_id' in request.session:
        messages.add_message(request, messages.INFO, "Looks like you didn't login!")
        return redirect('/')
    context = {
        'my_list': User.objects.get(id=request.session['user_id']).user_items.all(),
        'all_lists': List.objects.exclude(users = request.session['user_id']), 
    }



    return render(request, 'wish_list/dashboard.html', context)

def add_page(request):
    if not 'user_id' in request.session:
        messages.add_message(request, messages.INFO, "Looks like you didn't login!")
        return redirect('/')
    return render(request,'wish_list/create_list.html')

def data(request):
    response = List.objects.valid(request.POST)

    if response['valid']:
        user = User.objects.get(id=request.session['user_id'])
        new_item = List.objects.create(item = request.POST['item'], created_at = datetime.now(), updated_at = datetime.now())
        # For creating the many to many relationship
        new_item.save()
        new_item.users.add(user)
        # Save the change
        messages.add_message(request, messages.INFO, "You have successfully added a new item")
        return redirect('/dashboard')
    else:
        for error_message in response['errors']:
            # add messages one at a time and say that they are error messages IN THE messages variable
            messages.add_message(request, messages.ERROR, error_message)
        return redirect('wish_items/create') 
    
def wish_items(request, itemid):
    if not 'user_id' in request.session:
        messages.add_message(request, messages.INFO, "Looks like you didn't login!")
        return redirect('/')
    list_item = List.objects.get(id=itemid)
    context = {
        "item" : list_item.item,
        'created_by': list_item.users.first(),
        "joining_item" : list_item.users.all()
    }
    return render(request,'wish_list/item.html', context)

def join(request, itemid):
    # similar to the WillG lecture, keep it simple
    this_item = List.objects.get(id=itemid)
    new_user = User.objects.get(id=request.session['user_id'])
    this_item.users.add(new_user)
    messages.add_message(request, messages.INFO, "You have successfully joined a trip!")
    return redirect('/dashboard')

def delete(request, itemid):
    List.objects.get(id = itemid).delete()
    return redirect('/dashboard')


