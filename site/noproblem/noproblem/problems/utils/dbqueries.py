from noproblem.problems.models import Problem, Solves

def get_problems_solved(usr):
	solved_ok_idlist = Solves.objects.filter(user=usr).values_list('prob',flat=True).distinct()
	return Problem.objects.filter(id__in = solved_ok_idlist).all()
	
def get_problems_correct(usr):
	solved_ok_idlist = Solves.objects.filter(user=usr).filter(is_correct=True).values_list('prob',flat=True).distinct()
	return Problem.objects.filter(id__in = solved_ok_idlist).all()
	
def get_problems_cansolve(usr):
	solved_problems = get_problems_correct(usr)
	nextproblems = [];
	for i in solved_problems:
		nextproblems = nextproblems + list(Problem.objects.filter(requirements=i).all())
	return list(set(nextproblems) - set(solved_problems))
