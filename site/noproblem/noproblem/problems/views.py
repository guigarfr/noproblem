# Create your views here.
from noproblem.problems.models import User, Problem, Solves
from django.http import HttpResponse
from django.template import Context, loader
from django.db.models import F, Count
from django.shortcuts import render, get_object_or_404

from noproblem.problems.forms import UserSubmittedProblemForm, SolverFormSet

from django.forms.models import inlineformset_factory

def index(request):
    latest_prob_list = Problem.objects.order_by('-created_at')[:5]
    template = loader.get_template('indexpr.html')
    context = Context({
                      'latest_prob_list': latest_prob_list,
                      })
    return HttpResponse(template.render(context))

def detail(request, prob_id):
    pr = get_object_or_404(Problem, pk=prob_id)
    num = Solves.objects.filter(prob=prob_id).count()
    return render(request, 'stats.html', {'prob': pr,'num' : num})

def stats(request, prob_id):
    return HttpResponse("You're looking at the statistics of problem %s." % prob_id)


def user_solves(request, prob_id):
    
    pr = get_object_or_404(Problem, pk=prob_id)
            
    if request.POST:
        
        problem_form = UserSubmittedProblemForm(request.POST, instance=pr)
        if problem_form.is_valid():
            problem_form = problem_form.save(commit=False)
            solve_formset = SolverFormSet(request.POST, request.FILES, instance=pr)
            if solve_formset.is_valid():
                solve_formset.save()
                # Agregar una nueva tupla a resueltos
                return HttpResponseRedirect(reverse('stats', args=(pr.id,)))

    else:
        problem_form = UserSubmittedProblemForm(instance=pr)
        solve_formset = SolverFormSet(instance=pr)
    
    return render(request, "user_solves.html", {"prob": pr, "form":problem_form, "formset": solve_formset})
