# Create your views here.
from noproblem.accounts.models import UserProfile
from noproblem.problems.models import Problem, Solves, Area, SubArea
from noproblem.problems.forms import *
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
from noproblem.problems.utils.misc import topological_sort, is_number, calcprecision
from noproblem.problems.utils.sugiyama import problem_get_node_positions, sugiyama_graph_drawing_layering
from math import atan
from collections import defaultdict
from noproblem.problems.forms import ContactForm
from noproblem.problemforum.models import Thread

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


def tree(request, cat_id):
	#Parametros dibujo svg:
	# xradio=35
# 	yradio=25
# 	centerx=50
# 	centery=50
	xradio=55
	yradio=25
	centerx=60
	centery=60
	
	context = Context({})	
	if cat_id:
		categoria = get_object_or_404(Area, pk=cat_id)
		context['cat'] = categoria
		
	subareas=SubArea.objects.filter(area=categoria)
	if len(subareas)==0:
		context['notree'] = True
		return render(request, 'tree.html', context)
		
	problist = Problem.objects.filter(category__in = subareas).all()
	if len(problist)==0:
		context['notree'] = True
		return render(request, 'tree.html', context)
		
	dictposic = problem_get_node_positions(problist)
	layers = sugiyama_graph_drawing_layering(problist)
	map(lambda x:list(x),layers)
	numlayers = len(layers)
	
	dictlayers={}
	i=0
	for layer in layers:
		for prob in layer:
			dictlayers[prob] = i
		i=i+1
	
	edgemoddict = {}
	for p in problist:
		anglelist = []
		angledict = defaultdict(list)
		for padre in p.get_parents():
			pos = dictposic[p]
			pospadre = dictposic[padre]
			if pospadre[0] == pos[0]:
				angle = 0
			else:
				angle = atan(1.0*(pospadre[1] - pos[1])/(pospadre[0] - pos[0]))
			print 'Problem ' + p.title + ' has angle ' + str(angle) + ' with his parent ' + padre.title
			anglelist.append((p,padre,angle, dictlayers[prob]))
			angledict[angle].append(padre)
			edgemoddict[(p,padre)] = False
		# Evaluo los padres a ver si coinciden en angulo
		for a,plist in angledict.items():
			if len(plist)>1:
				layerp = map(lambda x: dictlayers[x], plist)
				print "Angulo " + str(a) + " problemas " + str(plist)
				print "Capas " + str(layerp)
				amodificar = plist[min([i for i, j in enumerate(layerp) if j == max(layerp)])]
				print "Quiero modificar el padre " + str(amodificar)
				edgemoddict[(p,amodificar)] = True
	print "Lista de caminos a modificar " + str(edgemoddict)
				
	# Minimum difference between nodes in the same level
	nlevel = max([x[1] for x in dictposic.values()])+1
	levelmin = [9999999999999]*nlevel
    
	for i in range(0,nlevel):
		xelems = sorted(list(set([t[0] for t in dictposic.values() if t[1] == i])))
		if len(xelems)>1:
			levelmin[i] = min([b-a for a, b in zip(xelems[:-1], xelems[1:])])
		else:
			levelmin[i] = xelems[0]
		print xelems,levelmin[i]
	xminlevel = min(levelmin)	
	print "El minimo era " + str(xminlevel)
	
	# Si mis elipses tienen radio (rx,ry), para que su distancia minima en x sea rx
	myfactor=1
	if xminlevel:
		myfactor=(centerx+xradio)*1.0/xminlevel
	newdict = dict([(x , (y[0]*myfactor,y[1])) for x,y in dictposic.items()])
	
	edges=[]
	for probs,tocurve in edgemoddict.items():
		edges.append((newdict[probs[0]],newdict[probs[1]],tocurve))
	
	print "Nuevos caminos: " + str(edges)
#	{% with 35 as xradio and 25 as yradio %}
# 	{% with 50 as centerx and 50 as centery %}
# 	{% with 250 as factorx and 100 as factory %}
# 	{% with 9 as textsize %}
	#Max and min x position and min difference
	xmax = newdict.items()[0][1][0]
	xmin = newdict.items()[0][1][0]
	for p,v in newdict.items():
		if v[0] > xmax:
			xmax = v[0]
		if v[0] < xmin:
			xmin = v[0]
	mywidth=xmax-xmin
	# Number of levels
	nlevel = max([x[1] for x in dictposic.values()])+1
	#Set context and render call
	context['pr_dict'] = newdict
	context['layer_list'] = layers
	context['nlayers'] = numlayers
	context['svgwidth'] = mywidth
	context['xradio'] = xradio
	context['yradio'] = yradio
	context['centerx'] = centerx
	context['centery'] = centery
	context['edges'] = edges

	print "A renderizar"
	return render(request, 'tree.html', context)

@login_required
def detail(request, prob_id):
    pr = get_object_or_404(Problem, pk=prob_id)
    
    # Problem data
    mydata = pr.data()
    nout=len(pr.solve(mydata))
    
    #hilo
    hilo = Thread.objects.filter(prob=prob_id)[0]
    #Set context and render call
    context = Context({
                      'prob': pr,
                      'probdata': mydata,
                      'cat': pr.category.area,
                      'nout': nout,
                      'hilo': hilo.pk,
                      })
    return render(request, 'detail.html', context)

@login_required 
def user_detail(request):
	# Obtener lista de problemas global
	all_problems = Problem.objects.all()
	solves_problemsolved=Solves.objects.select_related('user').filter(user=request.user)
	solved_problems=get_problems_solved(request.user)
	tosolve_problems = list(set(all_problems) - set(solved_problems))
	cansolve_problems=get_problems_cansolve(request.user)
	nextsolve_problems = list(set(tosolve_problems) - set(cansolve_problems))
	
	n_problems = Problem.objects.count()
	
	# Numero de resoluciones correctas e incorrectas global
	n_ok = solves_problemsolved.filter(is_correct = True).count()
	n_nok = solves_problemsolved.count() - n_ok
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
	for i in range(0,solves_problemsolved.count()):
		pr_id=solves_problemsolved[i].prob.id-1
		n_solved[pr_id] = n_solved[pr_id]+1
		n_solved_ok[pr_id] = n_solved_ok[pr_id]+solves_problemsolved[i].is_correct
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
	
	# Vector de listas de resoluciones
	if (n_solved_total > 0):
		solved_list_by_problem=n_problems * [None]
		for i in range(0,n_problems):
			solved_list_by_problem[i] = solves_problemsolved.filter(prob=i+1)
	else:
		solved_list_by_problem = []

	# Vector de identificador de problema por resolver
	if (n_solved_total > 0):
		solved_list_by_problem=n_problems * [None]
		for i in range(0,n_problems):
			solved_list_by_problem[i] = solves_problemsolved.filter(prob=i+1)
	
    #Set context and render call
	context = Context({
					  'num_resueltos': n_solved_total,
					  'num_resueltos_ok': n_solved_total_ok,
					  'prob_list': all_problems,
					  'prob_solved': solved_problems,
					  'prob_unsolved': tosolve_problems,
					  'prob_cansolve': cansolve_problems,
					  'prob_nextsolve': nextsolve_problems,
					  'tasa_acierto_por_problema': n_solved_pct_ok,
					  'tasa_acierto_global': n_pct_ok,
					  'nprob': n_problems,
                      'sprob_list_list': solved_list_by_problem,
                      })
	return render(request, 'user_detail.html', context)


@login_required    
def sendresult(request, prob_id):
	import ast

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
	
	mydata = pr.data()
	nout=len(pr.solve(mydata))
	
	# Set needed variables: user, prob, date, time, is_correct
	res_sent=[]
	for i in range(nout):
		newres = request.POST['result'+str(i)];
		print newres
		res_sent.append(newres)
		if res_sent[i]=='':
			correct=False	
	
	when = datetime.datetime.today()
   	solving_time = request.POST['time']
   	usuario=request.user.get_profile()
   	problem_data=request.POST['prdata']
   	if problem_data[0]=='[':
   		problem_data = ast.literal_eval(request.POST['prdata'])
   		map(str,problem_data)
   	
   	# Compute result
   	#To do: precision de res_ok, dos cifras significativas (caso particular de numeros entre 0 y 1)   	
   	
	print problem_data
	res_ok = pr.solve(problem_data)
	print "Resultados",res_sent,res_ok
	print "L1",len(res_ok)
	print "L2",len(res_sent)
	#Is the list the correct size?
	if( len(res_ok) != len(res_sent) ):
		print "Listas de distintos tamanyos"
		correct = False
	else:
		# Check if result is correct: TODO: deal with float numbers
		correct = False
		for i in range(len(res_ok)):
			if isinstance(res_ok[i], str):
				print "Es str"
				if res_ok[i] == res_sent[i]:
					correct = True
				else:
					correct = False
					break
			else:
				print "Es numero"
				#la precision esta hecha para que la primera cifra significativa no pueda variar (la segunda si)
				if abs(res_ok[i] - float(res_sent[i])) <= calcprecision(res_ok[i]):
					correct = True
				else:
					correct = False
					break
    
	# If not resolved before, add points to user
	if not pr.solved_by_user(usuario) and correct:
		usuario.credits = usuario.credits+pr.points
		usuario.save()
    
   	# Add new solve to database
	s = Solves(user=usuario, prob=pr,date=when, time=solving_time, is_correct=correct)
	s.save()
	
	# Always return an HttpResponseRedirect after successfully dealing
	# with POST data. This prevents data from being posted twice if a
	# user hits the Back button.
	return HttpResponseRedirect(reverse('problems:stats', args=(pr.id,)))

def stats(request, prob_id):
    pr = get_object_or_404(Problem, pk=prob_id)
    context = Context({
    				 'prob': pr,
    				 'cat': pr.category.area,
    				 })
    
    # Compute variables for context
    solves_list = Solves.objects.filter(prob=pr)
    context['solves_list'] = solves_list
    num=solves_list.count()
    
    if (num != 0):
		nok = solves_list.filter(is_correct=1).count()
		nfail = solves_list.count() - nok
		pctg_oks = nok/num
		pctg_fails = 1 - pctg_oks
		context['oks'] = nok
		context['fails'] = nfail
		context['pctg_oks'] = pctg_oks
		context['pctg_fails'] = pctg_fails
		
		# Calculate average solving time
		solving_times = solves_list.filter(is_correct=1).values_list('time')
		avg_time = datetime.time(0)
		if len(solving_times):
			for t in solving_times:
				avg_time = addTime(avg_time,t[0])
			mygm=time.gmtime((avg_time.hour*3600.0+avg_time.minute*60+avg_time.second)/nok)
			avg_time = datetime.time(mygm.tm_hour, mygm.tm_min, mygm.tm_sec)
			context['avg_time'] = avg_time
	
		# Create google pie chart
		chart = PieChart3D(250, 100)

		# Add some data
		chart.add_data([nok, nfail])

		# Assign the labels to the pie data
		chart.set_pie_labels(['OK', 'Fail'])
		
		context['chart_url'] = chart.get_url()
	    
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
    

def bienvenida(request):
	context = Context({
					 'colores_cuadros': ('#FA8072','#BDB76B','#4682B4','#F4A460'),
					 })	
	return render(request, 'bienvenida.html', context)
	
def contacto(request):
	if request.method == 'POST': 
		form = ContactForm(request.POST) 
		if form.is_valid():
			messages.success(request, 'El formulario ha sido enviado')
			cd = form.cleaned_data 
			email = EmailMessage('[connectacpc] Contacto: ' + cd['nombre'] + ' motivo: ' + cd['motivo'],
								 cd['message'] + "\n\nEnviado por: " + cd.get('email'),
								 cd.get('email'),
								 ['guigarfr@gmail.com','paulatuzon@gmail.com'],
								 headers={'Reply-To': cd.get('email')})
			email.send()
			return render_to_response('contacto_nop.html', {'form': form}, context_instance=RequestContext(request)) 
	else: 
		form = ContactForm() 
	return render_to_response('contacto_nop.html', {'form': form}, context_instance=RequestContext(request)) 	
		
		