# -*- coding: utf-8 -*-

from django.forms import ModelForm, HiddenInput
from noproblem.problems.models import Problem, Solves
from django.forms.models import inlineformset_factory
from django import forms

#MAX_INGREDIENTS = 20 para parametro extra al final del formset

SolverFormSet = inlineformset_factory(Problem,
                                      Solves,
                                      can_delete=False)

class UserSubmittedProblemForm(ModelForm):
    class Meta:
        model = Problem
        exclude = ('category', 'wording','points','created_at','updated_at','requirements','datos','solucion')

class SolverForm(ModelForm):
	class Meta:
		model = Solves
		widgets = {
        'user': HiddenInput(),
        'prob': HiddenInput(),
        'date': HiddenInput(),
        'time': HiddenInput(),
        }
        exclude = ('is_correct')
        
class RegistroUsuario(forms.Form): 
	nombre = forms.CharField(required=False, max_length=100,label='Nombre')
	email = forms.EmailField(label='E-mail')
	password = forms.CharField(label='Contraseña',widget=forms.PasswordInput) 



