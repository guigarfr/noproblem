#++++++++++++++++hiponetusa+++++++++++++
#Dados los dos catetos, halla la hipotenusa.

from random import randint
import constantes
import random
from math import pow, sqrt
import math

def hipotenusa_datos():
    lista=[]
    lista.append(randint(1,20))
    l1=0
    while (l1 < lista[0]):
        l1 = randint(2,20)
    lista.append(l1)
    return lista

def hipotenusa(lista):
    return sqrt(pow(lista[0],2)+lista[1]**2)

#++++++++++++++++trenes velocidad constante++++++++++
#De dos ciudades que estan a una distancia de d km salen dos trenes respectivamente, si el primero va a una velocidad
#en m/s y el segundo a otra en m/s, calcula cuando y donde se cruzaran.

def trenes_datos():
	lista=[]
	v1=randint(28,130)
	v2=randint(28,130)
	dist=randint(100,1000)
	lista.extend([v1,v2,dist])
	return lista

def trenes(lista):
	lista[0]=lista[0]*3.6
	lista[1]=lista[1]*3.6
	t=lista[2]/(lista[1]+lista[0])
	x=lista[0]*t
	return (x,t)

#++++++++++++++++plano inclinado 1++++++++++
#Desde una altura de 50 cm soltamos un objeto situado en un plano inclinado 30 con la horizontal. 
#El coeficiente de rozamiento entre el objeto y la superficie es 0,2. Determinen la velocidad con que llegara al suelo.

def plano1_datos():
	lista=[]
	altura=randint(20,100)
	angulo=randint(10,70)
	coef= random.randrange(1, 9, 1)	
	coef=float(coef)/10.0
	lista.extend([altura,angulo,coef])
	return lista

def plano1(lista):
	FR=-lista[2]*constantes.G*math.cos(math.radians(lista[1]))
	Px=constantes.G*math.sin(math.radians(lista[1]))
	a=FR+Px
	espacio=(float(lista[0])/100.0)/math.sin(math.radians(lista[1]))
	t=sqrt(2*espacio/a)
	v=a*t
	return v
	
 
#++++++++++++++++objeto hacia arriba++++++++++
#Guille se ha quedado encerrado en casa y no puede salir. Por suerte tenemos copia de sus llaves, asi que vamos 
#a su casa y se las tenemos que lanzar hasta el balcon, donde el esta para recogerlas. Si su balcon esta
#a 5 metros de donde vamos a lanzar las llaves, con que velocidad minima tendremos que lanzarlas para que lleguen a su altura?
#El dia en Valencia esta poco humedo, sin viento y casi sin polucion (extranyamente), asi que asume que el rozamiento con el aire
#es practicamente nulo.
 
def altura_datos():
	lista=[]
	altura=randint(2,50)
	lista.append(altura)
	return lista
	
def altura(lista):
	t=sqrt(lista[0]*2.0/constantes.G)
	v=t*constantes.G
	return v
	
	
#++++++++++++++++frenada++++++++++
#Un coche ve el semaforo ponerse en rojo cuando esta a 50 metros de el, y los peatones han empezado a pasar. 
#Si el motor de su coche es capaz de decelerar como maximo a 7 m/s2 (es la deceleracion de un coche normal), 
#cual es la velocidad maxima a la que puede ir antes de empezar a frenar para no atropellarlos?

def frenada_datos():
	lista=[]
	distancia=randint(20,60)
	lista.append(distancia)
	return lista

def frenada(lista):
	decel=7.0
	t=sqrt(lista[0]*2.0/decel)
	v=decel*t*3.6
	return v
	
 
 
 
 
 
 
 
 
 
 
 
 
 







