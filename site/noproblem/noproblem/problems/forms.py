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

class ContactForm(forms.Form): 
	motivo = forms.ChoiceField(widget = forms.Select(),
					 label = '¿Por qué quieres contactar con nosotros?',
                     choices = ([('error','He encontrado un error'),
                     			 ('sugerencia','Quiero sugerir un problema'),
                     			 ('otros','Otros') ]), required = True,)
	message = forms.CharField(widget = forms.widgets.Textarea(),label='Contenido del Mensaje') 


