# Create your views here.
from noproblem.accounts.models import UserProfile
from noproblem.problems.models import Problem, Solves
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
from django.db.models import Avg
import time, datetime, operator
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from noproblem.problems.utils.dbqueries import *
from noproblem.problems.utils.misc import topological_sort

####################################################
# 					GLOBAL VARS					   #
####################################################
precision = 1e-3

####################################################
#			  GENERIC PYTHON FUNCTIONS			   #
####################################################

def addTime(tm1, tm2):
    fulldate = datetime.datetime(100, 1, 1, tm1.hour, tm1.minute, tm1.second)
    fulldate = fulldate + datetime.timedelta(hours=tm2.hour,minutes=tm2.minute,seconds=tm2.second)
    return fulldate.time()

####################################################
#					  VIEWS						   #
####################################################

def index(request):
	latest_prob_list = Problem.objects.order_by('-created_at')[:5]
	
	#Set context and render call
	context = Context({
                      'latest_prob_list': latest_prob_list,
                      })
	return render(request, 'indexpr.html', context)


def tree(request):
    prlist = Problem.objects.all()
    
    #Set context and render call
    context = Context({
                      'pr_list': prlist,
                      })
    return render(request, 'tree.html', context)

@login_required
def detail(request, prob_id):
    pr = get_object_or_404(Problem, pk=prob_id)
    
    #Set context and render call
    context = Context({
                      'prob': pr,
                      })
    return render(request, 'detail.html', context)

@login_required 
def user_detail(request):
	# Obtener lista de problemas global
	solved_problems=Solves.objects.select_related('user').filter(user=request.user)
	all_problems = Problem.objects.all()
	n_problems = Problem.objects.count()
	
	# Numero de resoluciones correctas e incorrectas global
	n_ok = solved_problems.filter(is_correct = True).count()
	n_nok = solved_problems.count() - n_ok
	if (n_ok > 0):
		n_pct_ok = n_ok / n_problems
	else:
		n_pct_ok = 0
	if (n_nok > 0):
		n_pct_nok = n_nok / n_problems
	else:
		n_pct_nok = 0
		
	# Numero de resoluciones correctas e incorrectas para cada problema
	n_solved = [0] * n_problems
	n_solved_ok = [0] * n_problems
	for i in range(0,solved_problems.count()):
		pr_id=solved_problems[i].prob.id-1
		n_solved[pr_id] = n_solved[pr_id]+1
		n_solved_ok[pr_id] = n_solved_ok[pr_id]+solved_problems[i].is_correct
		n_solved_false = map(operator.sub, n_solved, n_solved_ok)
		
	n_solved_total = sum(x > 0 for x in n_solved)
	n_solved_total_ok = sum(x > 0 for x in n_solved_ok)

	# Porcentajes de resolucion de cada problema
	n_solved_pct_ok = [0.0] * n_problems
	for i in range(0,n_problems):
		if(n_solved[i] == 0):
			n_solved_pct_ok[i] = 0
		else:
			n_solved_pct_ok[i] = 1.0 * n_solved_ok[i] / n_solved[i]	
	n_solved_pct_nok = map(lambda x: 1 - x, n_solved_pct_ok)
	
	# Lista de identificadores de todos los problemas
	id_prob_all=map(lambda x: x-1, Problem.objects.values_list('id',flat=True))
	id_prob_solved_ok=map(lambda x: x-1, solved_problems.filter(is_correct=True).values_list('prob',flat=True).distinct())
	id_prob_tosolve = map(lambda x: int(x), set(id_prob_all) - set(id_prob_solved_ok))
	id_prob_cansolve = map(lambda x: x.id-1, get_problems_cansolve(request.user))
	id_prob_nextsolve = list(set(id_prob_tosolve) - set(id_prob_cansolve))
	
	# Lista de identificadores de los problemas resueltos
	id_prob_all=Problem.objects.values_list('id',flat=True)

	# Vector de listas de resoluciones
	if (n_solved_total > 0):
		solved_list_by_problem=n_problems * [None]
		for i in range(0,n_problems):
			solved_list_by_problem[i] = solved_problems.filter(prob=i+1)
	else:
		solved_list_by_problem = []

	# Vector de identificador de problema por resolver
	if (n_solved_total > 0):
		solved_list_by_problem=n_problems * [None]
		for i in range(0,n_problems):
			solved_list_by_problem[i] = solved_problems.filter(prob=i+1)


    #Set context and render call
	context = Context({
					  'num_resueltos': n_solved_total,
					  'num_resueltos_ok': n_solved_total_ok,
					  'prob_list': all_problems,
					  'prob_unsolved_id': id_prob_tosolve,
					  'prob_cansolve_id': id_prob_cansolve,
					  'prob_nextsolve_id': id_prob_nextsolve,
					  'tasa_acierto_por_problema': n_solved_pct_ok,
					  'tasa_acierto_global': n_pct_ok,
					  'nprob': n_problems,
                      'sprob_list_list': solved_list_by_problem,
                      })
	return render(request, 'user_detail.html', context)


@login_required    
def sendresult(request, prob_id):

	# Get problem object from database
	# Problem already exists as we come from detail view
	pr = get_object_or_404(Problem, pk=prob_id)
    
#	try:

    	# User exists?
    	#selected_choice = p.choice_set.get(pk=request.POST['choice'])
    	
    	# Is date in the future?
    	
    	#return render_to_response('polls/detail.html', {
        #    'poll': p,
        #    'error_message': "You didn't select a choice.",
        #}, context_instance=RequestContext(request))

    	
#    except (KeyError, Problem.DoesNotExist)
		# Redisplay the poll voting form.
        #return render_to_response('polls/detail.html', {
        #    'poll': p,
        #    'error_message': "You didn't select a choice.",
        #}, context_instance=RequestContext(request))
#    else:		

	# Set needed variables: user, prob, date, time, is_correct
	res_sent = request.POST['result']
   	when = datetime.datetime.today()
   	solving_time = request.POST['time']
   	usuario=request.user.get_profile()
    
   	# Compute result
   	# TODO: De momento solo para un resultado, pero es una LISTA!!!!!
   	
   	if( res_sent == ""):
   		correct = False
   	else:
		res_list = map(float, res_sent.split(","))
		res_ok = pr.solve(res_list)
		#Is the list the correct size?
		if( len(res_ok) != len(res_sent) ):
			correct = False
		else:
			# Check if result is correct: TODO: deal with float numbers
			for i in range(len(res_ok)):
				if res_ok[i] - float(res_sent[i]) < 1e-3:
					correct = True
				else:
					correct = False
					break
    	
   	# Add new solve to database
	s = Solves(user=usuario, prob=pr,date=when, time=solving_time, is_correct=correct)
	s.save()
	
	# Always return an HttpResponseRedirect after successfully dealing
	# with POST data. This prevents data from being posted twice if a
	# user hits the Back button.
	return HttpResponseRedirect(reverse('problems:stats', args=(pr.id,)))

def stats(request, prob_id):
    pr = get_object_or_404(Problem, pk=prob_id)
    
    # Compute variables for context
    solves_list = Solves.objects.filter(prob=pr)
    num=solves_list.count()
    if (num != 0):
		nok = solves_list.filter(is_correct=1).count()
		nfail = solves_list.count() - nok
		pctg_oks = nok/num
		pctg_fails = 1 - pctg_oks
		
		# Calculate average solving time
		solving_times = solves_list.values_list('time')
		avg_time = datetime.time(0)
		for t in solving_times:
			avg_time = addTime(avg_time,t[0])    	
		avg_time = datetime.time(avg_time.hour/num,avg_time.minute/num,avg_time.second/num)
	
		# Create google pie chart
		chart = PieChart3D(250, 100)

		# Add some data
		chart.add_data([nok, nfail])

		# Assign the labels to the pie data
		chart.set_pie_labels(['OK', 'Fail'])
		
		#Set context and render call
		context = Context({
    				      'prob': pr,
                      	  'solves_list': solves_list,
                      	  'oks': nok,
                      	  'fails': nfail,
                      	  'pctg_oks': pctg_oks,
                    	  'pctg_fails': pctg_fails,
                    	  'avg_time' : avg_time,
                    	  'chart_url': chart.get_url(),
                      	  })
                      
    else:
    	context = Context({
					      'prob': pr,
                      	  'solves_list': solves_list,
                      	  })
    
    return render(request, 'stats.html', context)

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
    
    #Set context and render call
	context = Context({
					  'form': problem_form,
                      'formset': solve_formset,
                      })
    return render(request, 'user_solves.html', context)
    
				
			
		
		
		