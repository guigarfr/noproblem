# Create your views here.
from noproblem.problems.models import User, Problem, Solves
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.db.models import F, Count
from django.shortcuts import render, get_object_or_404, render_to_response
from noproblem.problems.forms import UserSubmittedProblemForm, SolverFormSet
from django.core.context_processors import csrf
from django.template import RequestContext
from django.core.urlresolvers import reverse
from pygooglechart import PieChart3D, PieChart2D
from noproblem import settings


def index(request):
    latest_prob_list = Problem.objects.order_by('-created_at')[:5]
    template = loader.get_template('indexpr.html')
    context = Context({
                      'latest_prob_list': latest_prob_list,
                      })
    return HttpResponse(template.render(context))

def detail(request, prob_id):
    pr = get_object_or_404(Problem, pk=prob_id)
    return render(request, 'detail.html', {'prob': pr})

def stats(request, prob_id):
    pr = get_object_or_404(Problem, pk=prob_id)
    solves_list = Solves.objects.filter(prob=pr)
    num=solves_list.count()
    template = loader.get_template('stats.html')
    nok = solves_list.filter(is_correct=1).count()
    nfail = solves_list.count() - nok
    pctg_oks = nok/num
    pctg_fails = 1 - pctg_oks
    # Create google pie chart
    chart = PieChart3D(250, 100)

    # Add some data
    chart.add_data([nok, nfail])

    # Assign the labels to the pie data
    chart.set_pie_labels(['OK', 'Fail'])
    context = Context({
    				  'prob': pr,
                      'solves_list': solves_list,
                      'oks': nok,
                      'fails': nfail,
                      'pctg_oks': pctg_oks,
                      'pctg_fails': pctg_fails,
                      'chart_url': chart.get_url(),
                      })
    return HttpResponse(template.render(context))

def solve(request, prob_id):
    pr = get_object_or_404(Problem, pk=prob_id)

    if request.POST:
        
        problem_form = UserSubmittedProblemForm(request.POST, instance=pr)
        if problem_form.is_valid():
            problem_form = problem_form.save(commit=False)
            solve_formset = SolverFormSet(request.POST, instance=pr)
            if solve_formset.is_valid():
                solve_formset.save()
                # Agregar una nueva tupla a resueltos
                return HttpResponseRedirect(reverse('problems:stats', args=(pr.id,)))

    else:
        problem_form = UserSubmittedProblemForm(instance=pr)
        solve_formset = SolverFormSet(instance=pr)
    
    #c.update({"form":problem_form, "formset": solve_formset})
    return render_to_response('user_solves.html', {"form":problem_form, "formset": solve_formset}, context_instance=RequestContext(request))
    #return render(request, "user_solves.html", {"form":problem_form, "formset": solve_formset})
