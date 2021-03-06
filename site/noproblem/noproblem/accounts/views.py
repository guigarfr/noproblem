from django.contrib import auth
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from noproblem.accounts.forms import RegistroUsuario
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib import messages

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

REDIRECT_FIELD_NAME = "next"

def register_user(request,  next_page=None, 
					template_name='auth.html', 
					redirect_field_name=REDIRECT_FIELD_NAME):
	if request.method =='POST':
		form = RegistroUsuario(request.POST)
		RegistroUsuario(request.POST)
		redirect_to = request.REQUEST.get(redirect_field_name, '') 
		if form.is_valid():
			user = form.save()
			passwd = form.clean_password2()
			messages.success(request, 'Su usuario ha sido registrado')
			new_user = auth.authenticate(username=form.cleaned_data['username'],
                                    password=passwd)
			if user is not None:
				if user.is_active:
					auth.login(request, new_user)
				else:
					state = "Your account is not active, please contact the site admin."
					# Redirigir a contacto??
					HttpResponseRedirect(reverse('contacto'))
			if redirect_to:
				return HttpResponseRedirect(redirect_to) 
			elif next_page is None:
				return render(request, template_name, {'title': _('Logged out')})
			else: 
				# Redirect to this page until the session has been cleared. 
				return HttpResponseRedirect(next_page or request.path)
		else:
			return render(request, 'register.html', {'form': form})
	else:
		form = RegistroUsuario()
		return render(request, 'register.html', {'form': form})


def logout(request, next_page=None, 
					template_name='logged_out.html', 
					redirect_field_name=REDIRECT_FIELD_NAME):
	"Logs out the user and displays 'You are logged out' message." 
	from django.contrib.auth import logout 
	logout(request) 
	print "Estoy en logout " + str(next_page) + ", " + redirect_field_name + ", " + template_name
	redirect_to = request.REQUEST.get(redirect_field_name, '') 
	if redirect_to: 
		return HttpResponseRedirect(redirect_to) 
	elif next_page is None:
		return render(request, template_name, {'title': _('Logged out')})
	else: 
		# Redirect to this page until the session has been cleared. 
		return HttpResponseRedirect(next_page or request.path)

