# Create your views here.
from noproblem.problems.models import Problem, Resultados
from django.http import HttpResponse
from django.template import Context, loader
from django.db.models import F, Count
from django.shortcuts import render, get_object_or_404

def index(request):
    latest_prob_list = Problem.objects.order_by('-created_at')[:5]
    template = loader.get_template('indexpr.html')
    context = Context({
                      'latest_prob_list': latest_prob_list,
                      })
    return HttpResponse(template.render(context))

def detail(request, prob_id):
    pr = get_object_or_404(Problem, pk=prob_id)
    num = Resultados.objects.filter(prob=prob_id).count()
    return render(request, 'stats.html', {'prob': pr,'num' : num})

def stats(request, prob_id):
    return HttpResponse("You're looking at the statistics of problem %s." % prob_id)
