def topological_sort(problem_list):
    """Perform topological sort.
       items is a list of items to be sorted.
       partial_order is a list of pairs. If pair (a,b) is in it, it means
       that item a should appear before item b.
       Returns a list of the items in one of the possible orders, or None
       if partial_order contains a loop.
    """
	
    def add_node(arcs_array, problem):
        """Add a node to the graph if not already exists."""
        if not arcs_array.has_key(problem.id):
            arcs_array[problem.id] = 0 # 0 = number of arcs coming into this node.
	
    def add_arc(arcs_array, problem_from, problem_to):
        """Add an arc to a graph. Can create multiple arcs.
           The end nodes must already exist."""
        # graph[fromnode].append(tonode)
        # Update the count of incoming arcs in tonode.
        arcs_array[problem_to.id] = arcs_array[problem_to.id] + 1
	
    # step 1 - Crear entradas en el diccionario para cada nodo.
    #          al tiempo, buscar raices: nodos sin dependencia con los nodos de la lista
    arcs_array = {}
    roots=[]
    queryset_list = Problem.objects.filter(pk__in=map(lambda x: x.id, problem_list))
    for v in problem_list:
    	if(list(set(v.requirements.all()) & set(problem_list)) == []):
			roots.append(v)
    	add_node(arcs_array, v)
    
    # Step 2 - find all roots: no tienen dependencias con los problemas de la lista    
    for v in problem_list:
        for a in v.get_children():
        	if v in problem_list:
        		add_arc(arcs_array, v, a)
    print arcs_array
    
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
        for child in root.get_children():
        	if child in problem_list:
        		arcs_array[child.id] = arcs_array[child.id] - 1
        		if arcs_array[child.id] == 0:
        			roots.append(child)
        del arcs_array[root.id]
    if len(arcs_array.items()) != 0:
        # There is a loop in the input.
        return None
    return sorted