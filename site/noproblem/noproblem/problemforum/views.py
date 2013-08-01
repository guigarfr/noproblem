# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from noproblem.problemforum.models import Thread, Post
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, render_to_response
from noproblem.settings import MEDIA_ROOT, MEDIA_URL
from noproblem.problemforum.forms import PostForm
from noproblem.accounts.models import UserProfile
from django.http import HttpResponseRedirect
from django import forms
from django.template import Context
from django.db.models import F


def add_csrf(request, ** kwargs):
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d

def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1
    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items

def forum(request):
    """Listing of threads."""
    threads = Thread.objects.order_by("-prob__created_at")
    threads = mk_paginator(request, threads, 20)
    return render(request, "forum.html", {"threads":threads})
    
def thread(request, pk):
	"""Listing of posts in a thread."""
	user =  UserProfile.objects.get(user=request.user)
	thread = Thread.objects.get(pk=pk)
	prob = thread.prob
	title = prob.title
	if prob.solved_by_user(user):
		posts = Post.objects.filter(thread=pk).order_by("created")
		posts = mk_paginator(request, posts, 15)
		print prob.pk
		context = Context({
			"posts":posts,
			"title":title,
			"pk":pk,
			"media_url":MEDIA_URL,
			"pr":prob,
			})
		return render(request, "thread.html", context)
	else:
		context = Context({
			'pk' : pk,
			'unsolved' : True,
			"title":title,
			"pr":prob,
			})
		return render(request, "thread.html", context)
		
		
# Pagar entrada a foro
def payforumentrance(request, pk):
	creditsperentrance = 1
	user =  UserProfile.objects.get(user=request.user)
	prob = Thread.objects.get(pk=pk).prob
	title = prob.title
	if user.credits>=creditsperentrance:
		posts = Post.objects.filter(thread=pk).order_by("created")
		posts = mk_paginator(request, posts, 15)
		user.credits = F('credits') - creditsperentrance
		user.save()
		context = Context({
			"posts":posts,
			"title":title,
			"pk":pk,
			"media_url":MEDIA_URL,
			"pr":prob, 
			})
		return render(request, "thread.html", context)
	else:
		context = Context({
			'pk' : pk,
			'unsolved' : True,
			'message' : "No tienes suficientes créditos para entrar al foro",
			'pr': prob,
			'title': title,
			})
		return render(request, "thread.html", context)
		
# Actions: post

def post(request, ptype, pk):
    """Display a post form."""
    action = reverse("forum:%s" % ptype, args=[pk])
    if ptype == "new_message":
        title = "Haz una pregunta del foro"
        subject = Thread.objects.get(pk=pk).prob.title
        form = PostForm()
        form.fields['username'].widget = forms.HiddenInput()
    if ptype == "reply":
        title = "Contesta a una pregunta del foro"
        post_to_reply = Post.objects.get(pk=pk)
        subject = post_to_reply.thread.prob.title
        form = PostForm(initial={'username': post_to_reply.creator.user.username})
    return render(request, "post.html", {"subject":subject,
        "action":action, "title":title, "form":form})

def reply(request, pk):
    """Reply to a thread."""
    p = request.POST
    if p["message"]:
    	prev = Post.objects.get(pk=pk)
        thread = prev.thread
        user = UserProfile.objects.get(user=request.user)
        post = Post.objects.create(thread=thread, body=p["message"], creator=user, previous=prev)
    return HttpResponseRedirect(reverse("forum:thread", args=[thread.pk]) + "?page=last")

def new_message(request, pk):
    """New message in a thread."""
    p = request.POST
    if p["message"]:
        thread = Thread.objects.get(pk=pk)
        user = UserProfile.objects.get(user=request.user)
        post = Post.objects.create(thread=thread, body=p["message"], creator=user)
    return HttpResponseRedirect(reverse("forum:thread", args=[pk]) + "?page=last")




