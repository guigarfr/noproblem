
lista=[[1],[2,1],[3,1],[4,1],[5,2,3],[6,2,3],[7,3],[8,3],[9,7,1]]
lista2=[[1],[2,1],[3,1],[4,1],[5,2,3],[6,2,3],[7,3],[8,3],[9,7,1],[10,1,2,3,8,9]]

def genera_pares(prob_padres):
#prob_padres es una lista (que llamamos lista arriba) 
#donde el primer elemento es el indice el problema y los demas son los problemas de los que depende
	pares=[]
	for i in prob_padres:
		len_sublist = len(i)
		if len_sublist > 1:
			for j in range(1,len(i)):
				par =[i[j],i[0]]
				pares.append(par)
	return pares

def numero_problemas(prob_padres):
	cuantos=len(prob_padres)
#cuantos es un entero que te dice cuantos problemas hay en total para hacer el arbol
	elementos=[]
	for i in range (0,cuantos):
		elementos.append(i+1)
	return elementos
	
#A la funcion topological_sort le pasaremos pares y elementos, que son las listas que devuelven las dos anteriores funciones


def topological_sort(items, partial_order):
    """Perform topological sort.
       items is a list of items to be sorted.
       partial_order is a list of pairs. If pair (a,b) is in it, it means
       that item a should appear before item b.
       Returns a list of the items in one of the possible orders, or None
       if partial_order contains a loop.
    """

    def add_node(graph, node):
        """Add a node to the graph if not already exists."""
        if not graph.has_key(node):
            graph[node] = [0] # 0 = number of arcs coming into this node.

    def add_arc(graph, fromnode, tonode):
        """Add an arc to a graph. Can create multiple arcs.
           The end nodes must already exist."""
        graph[fromnode].append(tonode)
        # Update the count of incoming arcs in tonode.
        graph[tonode][0] = graph[tonode][0] + 1

    # step 1 - create a directed graph with an arc a->b for each input
    # pair (a,b).
    # The graph is represented by a dictionary. The dictionary contains
    # a pair item:list for each node in the graph. /item/ is the value
    # of the node. /list/'s 1st item is the count of incoming arcs, and
    # the rest are the destinations of the outgoing arcs. For example:
    #           {'a':[0,'b','c'], 'b':[1], 'c':[1]}
    # represents the graph:   c <-- a --> b
    # The graph may contain loops and multiple arcs.
    # Note that our representation does not contain reference loops to
    # cause GC problems even when the represented graph contains loops,
    # because we keep the node names rather than references to the nodes.
    graph = {}
    for v in items:
        add_node(graph, v)
    for a,b in partial_order:
        add_arc(graph, a, b)

    # Step 2 - find all roots (nodes with zero incoming arcs).
    roots = [node for (node,nodeinfo) in graph.items() if nodeinfo[0] == 0]

    # step 3 - repeatedly emit a root and remove it from the graph. Removing
    # a node may convert some of the node's direct children into roots.
    # Whenever that happens, we append the new roots to the list of
    # current roots.
    sorted = []
    while len(roots) != 0:
        # If len(roots) is always 1 when we get here, it means that
        # the input describes a complete ordering and there is only
        # one possible output.
        # When len(roots) > 1, we can choose any root to send to the
        # output; this freedom represents the multiple complete orderings
        # that satisfy the input restrictions. We arbitrarily take one of
        # the roots using pop(). Note that for the algorithm to be efficient,
        # this operation must be done in O(1) time.
        root = roots.pop()
        sorted.append(root)
        for child in graph[root][1:]:
            graph[child][0] = graph[child][0] - 1
            if graph[child][0] == 0:
                roots.append(child)
        del graph[root]
    if len(graph.items()) != 0:
        # There is a loop in the input.
        return None
    return sorted

#sorted es un lista donde cada elemento no tiene como padre ninguno de los elementos que van detras de el en la lista


def genera_niveles(pares,orden):
#pares es la lista de pares que devuelve la funcion genera_pares
#orden es la lista que devuelve la funcion topological_sort
	niveles={1:0}
	#niveles.update({'item3': 3})
	#he creado una lista donde por defecto cada elemento de orden esta en un nivel
	for i in range (1,len(orden)):
		guarda=[]
		for n in range (1,i+1):
			for j in pares:
				if j==[orden[i-n],orden[i]]:
					guarda.append(orden[i-n])	
		take=max(guarda)
		new=niveles[take]
		niveles.update({orden[i] : new+1})
	return niveles	
	
pares=genera_pares(lista2)
elementos=numero_problemas(lista2)
order=topological_sort(elementos,pares)
print pares
print elementos
print order
print genera_niveles(pares,order)
#niveles es un diccionario donde que te dice cada elemento en que nivel esta

###Resumen:
###La funcion genera_pares tiene como input la lista donde el primer elemento es el label del problema 
#y los demas son los problemas de los que depende. el output son los pares (padre,hijo)
###La funcion numero_problemas tiene como output una lista desde 0 al numero de problemas que tengamos, 
#esta lista la requiere la funcion topological_sort que nos bajamos de internet
###La funcion general_niveles tiene como input el output de la funcion topological_sort (una lista
#donde cada elemento depende de alguno de los anteriores pero no de los posteriores) y la lista de pares,
#y tiene como output el diccionario que te dice cada nodo en que nivel esta {nodo:nivel}


