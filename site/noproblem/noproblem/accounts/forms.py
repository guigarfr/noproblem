# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from noproblem.accounts.models import UserProfile
from django import forms

class RegistroUsuario(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user