from noproblem.problems.models import Problem, Solves

def get_problems_solved(usr):
	solved_idlist = Solves.objects.filter(user=usr).values_list('prob',flat=True).distinct()
	return Problem.objects.filter(id__in = solved_idlist).all()
	
def get_problems_correct(usr):
	solved_ok_idlist = Solves.objects.filter(user=usr).filter(is_correct=True).values_list('prob',flat=True).distinct()
	return Problem.objects.filter(id__in = solved_ok_idlist).all()
	
def get_problems_cansolve(usr):
	all_problems = Problem.objects.all()
	solved_ok_problems = get_problems_correct(usr)
	initial_problems = all_problems.filter(requirements=None).all()
	nextproblems = list(initial_problems)
	for i in solved_ok_problems:
		nextproblems = list(nextproblems) + list(all_problems.filter(requirements=i).all())
	return list(set(nextproblems) - set(solved_ok_problems))
