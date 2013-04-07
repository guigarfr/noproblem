# -*- coding: utf-8 *-

from django import forms

class ContactForm(forms.Form): 
	nombre = forms.CharField(required=False, max_length=100,label='Nombre')
	email = forms.EmailField(label='E-mail')
	motivo = forms.ChoiceField(widget = forms.Select(),
					 label = '¿Por cuál de los servicios quieres contactar con nosotros?',
                     choices = ([('divulgacion','Divulgación'),
                     			 ('didactica','Didáctica'),
                     			 ('desarrollo','Desarrollo'),
                     			 ('preg_semanal','Pregunta Semanal'),
                     			 ('otros','Otros') ]), required = True,)
	message = forms.CharField(widget = forms.widgets.Textarea(),label='Contenido del Mensaje') 
