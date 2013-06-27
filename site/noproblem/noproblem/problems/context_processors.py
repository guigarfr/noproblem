
def categorias(request):
	from noproblem.problems.models import Area
	cats=Area.objects.all()
	return {'categorias': cats}