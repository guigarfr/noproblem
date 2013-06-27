from django.contrib import auth
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

def login_user(request):
    state = "Please log in below..."
    username = password = ''
    redirect_to = request.REQUEST.get('next', '')
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        next = request.POST.get('next')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                state = "You're successfully logged in!"
                return HttpResponseRedirect(redirect_to)
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
    context = {'state':state, 'username': username, 'next': redirect_to}
    context.update(csrf(request))
    return render_to_response('auth.html',context)

def logout_user(request):
    auth.logout(request)
    # Redirect to a success page.
    redirect_to = request.REQUEST.get('next', '')
    return HttpResponseRedirect(redirect_to)
    

