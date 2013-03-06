from django import forms
from noproblem.problems.models import Problem, Solves
from django.forms.models import inlineformset_factory

#MAX_INGREDIENTS = 20 para parametro extra al final del formset

SolverFormSet = inlineformset_factory(Problem,
                                      Solves,
                                      can_delete=False)

class UserSubmittedProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        exclude = ('category', 'created_at','updated_at','requirements','datos','solucion')
