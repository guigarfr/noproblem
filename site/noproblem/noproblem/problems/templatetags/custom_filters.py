from django import template

register = template.Library()
	
class SetVarNode(template.Node):
 
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value
 
    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""
 
def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])
 
register.tag('set', set_var)

@register.filter
def lookup(d, key):
    return d[key]


@register.filter
def solve(obj, data):
	return obj.solve(data)

@register.filter
def keyvalue(dict, key):    
    return dict[key]

@register.filter
def multiplyperfactor(num,fac):    
    return int(num*fac)

@register.filter
def add(num,fac):    
    return num+fac

@register.filter
def substract(num,fac):    
    return num-fac

@register.filter
def half(num):    
    return num/2

@register.filter
def issolved(obj, user):
	return obj.solved_by_user(user)

@register.filter
def nexttosolve(obj, user):
	return obj.is_next_to_solve(user)

@register.filter
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range( value )
