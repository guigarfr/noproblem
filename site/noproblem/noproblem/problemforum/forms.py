from django import forms
TO_HIDE_ATTRS = {'class': 'hidden'}

class PostForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs=TO_HIDE_ATTRS))
    message = forms.CharField(widget=forms.Textarea, label='Mensaje')
