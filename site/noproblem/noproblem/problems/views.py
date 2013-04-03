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
import time,datetime
from django.contrib.auth.decorators import login_required

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

@login_required
def detail(request, prob_id):
    pr = get_object_or_404(Problem, pk=prob_id)
    
    #Set context and render call
    context = Context({
                      'prob': pr,
                      })
    return render(request, 'detail.html', context)
    
@login_required
def sendresult(request, prob_id, data, result, solving_time):

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

	# Set needed variables: result, date, time
	res_sent = request.POST['result']
   	when = data
   	#solving_time = 
    
   	# Compute result
   	res_ok = pr.solve(data)
    
   	# Check if result is correct: TODO: deal with float numbers
   	if res_ok - res_sent < 1e-3:
   		correct = true
   	else:
   		correct = false
    	
   	# Add new solve to database
	s = Solve(user=usr_sent, prob=pr,date=when, time=solving_time, is_correct=correct)
	s.save()
	
	# Always return an HttpResponseRedirect after successfully dealing
	# with POST data. This prevents data from being posted twice if a
	# user hits the Back button.
	return HttpResponseRedirect(reverse('problems.views.stats', args=(pr.id,)))

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