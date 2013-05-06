import math
from noproblem.problems.models import Problem

def sugiyama_graph_drawing_layering(graph):
	# Graph MUST be directed and acyclic. If it's not acyclic, first its loops must be
	# removed
	V = list(graph)
	V1 = set()
	V2 = set()
	currentLayer = 0
	LayerElems = []
	while len(V1) < len(V):
		print "Layer:",currentLayer
		check4sink = list(set(V) - set(V1))
		LayerElems.append(set())
		for node in check4sink:
			if node not in V2 and set(node.get_children()).issubset(V2):
				V1.add(node)
				print "SINK:",node
				LayerElems[currentLayer].add(node)
		V2 = V2.union(V1)
		print "Nuevos sinks:",V2
		currentLayer = currentLayer+1
	return LayerElems


def graph_drawing_cross_minimization_median_method(fixed_layer_dict, free_layer):
	free_layer_pos = [None]*len(free_layer)
	degree = [None]*len(free_layer)
	currNode = 0
	for node in free_layer:
		hijos = node.get_children()
		nhijos = hijos.count()
		degree[currNode] = nhijos
		if hijos:
			if nhijos == 1:
				print "1 hijo!"
				free_layer_pos[currNode] = fixed_layer_dict[hijos[0]]
			else:
					print str(nhijos) + " hijos!"
					num = (nhijos-1)/2.0
					hijosmedian = map(lambda x: fixed_layer_dict[x], hijos)
					hijosmedian.sort()
					hijosmedian
					newpos =  (hijosmedian[int(math.floor(num))] + hijosmedian[int(math.ceil(num))])/2.0
					free_layer_pos[currNode] = newpos	
		else:
			print "sin hijos!"
			free_layer_pos[currNode] = 0
		print "siguiente nodo"
		print free_layer_pos
		currNode = currNode + 1
		
	for i in set(free_layer_pos):
	# Reasignar los nodos que tengan posiciones repetidas segun degree
	#
	# Repetidos con valor 1: rep = [i for i in range(len(array)) if array[i] == 1]
		rep = [x for x in range(len(free_layer_pos)) if free_layer_pos[x] == i]
		# si esta repetido len(rep) > 1
		if len(rep)>1:
			print "Hay repetidos"
			#
			# Grados de estos nodos: dg = map(lambda x: degree[x], rep)
			dg = map(lambda x: degree[x], rep)
			#
			grados = list(set(dg))
			# Hago un zip para saber siempre a que nodo pertenece el grado
			nodes = zip(rep,dg)
			
			#Cojo grados impares y pares
			imp =  [x for x in nodes if x[1]%2 == 1]
			par =  [x for x in nodes if x[1]%2 == 0]
			
			# Las ordeno. Esto es para que si hay dos con el mismo grado, esten juntos
			# Igual no es necesario, mas aleatorio si no se hiciera
			imp.sort(key=lambda x: x[1])
			par.sort(key=lambda x: x[1])
			
			# Busco limites: cuales tengo???
			sups = [x for x in free_layer_pos if x > i]
			mins = [x for x in free_layer_pos if x < i]
			if len(sups):
				limsup = min(sups)
			else:
				limsup = float("infinity")
			if len(mins):
				liminf = max(mins)
			else:
				liminf = float("-infinity")
			
			# Establezco el orden de los nodos
			orden = imp + par
			# en orden tengo pares (posicion, grado) ordenados por grado impar/par y dentro de cada grupo, por grado
					
			# Caso: no hay limites
			#        Reparto los nodos a distancia 1 con centro en POS
			mymin = i - (len(orden) - 1)/2.0
			for j in orden:
				free_layer_pos[j[0]] = mymin
				mymin = mymin + 1
			
			# Caso: posicion entre dos limites, A y B
			#        caso con limites infinito, ajustado al rango (A,B)
			if not liminf == float("-Inf") and not limsup == float("Inf"):
				oldrange = free_layer_pos[orden[len(orden)-1][0]] - free_layer_pos[orden[0][0]]
				newrange = -1
				dist = 1
				while (newrange <= 0):
					newrange = (limsup-dist) - (liminf+dist)
					dist = dist/2
				if(newrange > oldrange):
					# Adjust range
					fac = newrange/oldrange
					for j in orden:
						free_layer_pos[j[0]] = (free_layer_pos[j[0]]*fac)
						free_layer_pos[j[0]] = free_layer_pos[j[0]] + (liminf+1) - free_layer_pos[orden[0][0]]
			else:
				if liminf == float("-Inf") and not limsup == float("Inf"):
					# Caso: no hay limite inferior, pero si superior B
					# Muevo nodos hacia la izquierda, si necesario
					if free_layer_pos[orden[(len(orden)-1)][0]] >= limsup:
						howmuch = free_layer_pos[orden[(len(orden)-1)][0]] - (limsup - 1)
						for j in orden:
							free_layer_pos[j[0]] = free_layer_pos[j[0]] - howmuch
				
				if not limsup == float("Inf") and limsup == float("Inf"):
					# Caso: no hay limite superior, pero si inferior A
					# Muevo nodos a la derecha, si necesario
					if free_layer_pos[orden[0][0]] <= liminf:
						howmuch = (liminf + 1) - free_layer_pos[orden[0][0]]
						for j in orden:
							free_layer_pos[j[0]] = free_layer_pos[j[0]] + howmuch
	
	return free_layer_pos


def problem_get_node_positions(myprob):
	mylist = sugiyama_graph_drawing_layering(myprob)
	
	mypos = range(0,len(mylist[0]))
	i = 0
	mydict = dict()
	
	for i in range(0,len(mylist)-1):
		print "Estoy en " + str(i)
		newdict = dict(zip(mylist[i],mypos))
		mydict = dict(mydict.items() + newdict.items())
		print mydict
		mypos=graph_drawing_cross_minimization_median_method(mydict,mylist[i+1])
		print mypos
		i = i + 1
	
	#Agrego los del nodo/s raiz
	newdict = dict(zip(mylist[i],mypos))
	mydict = dict(mydict.items() + newdict.items())
	print mydict
	
	#
	# NORMALIZAR DISTANCIAS PARA QUE LA MINIMA SEA n
	# (no hace falta?) luego puedo agrandar el arbol?
	# O si que hace falta para poder saber que tamanyo poner a un nodo
	mylist = sorted(list(set(mydict.values())))
	newmin = min([j-i for i, j in zip(mylist[:-1], mylist[1:])])
	if(newmin < 1):
		mydict = dict([ (k,v/newmin) for (k,v) in mydict.items() ]).values()
	
	return mydict