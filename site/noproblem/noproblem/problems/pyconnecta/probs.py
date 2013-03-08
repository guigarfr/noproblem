#++++++++++++++++hiponetusa+++++++++++++
#Dados los dos catetos, halla la hipotenusa.
import sys
import os

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

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
#Un coche ve el semaforo ponerse en rojo cuando esta a 20 metros de el, y los peatones han empezado a pasar. 
#Si el motor de su coche es capaz de decelerar como maximo a 6 m/s2 (es la deceleracion de un coche normal), 
#a cuantos km/h podra ir como maximo el coche antes de empezar a frenar para no atropellarlos?

def frenada_datos():
	lista=[]
	distancia=randint(20,60)
	lista.append(distancia)
	return lista

def frenada(lista):
	decel=6.0
	t=sqrt(lista[0]*2.0/decel)
	v=decel*t*3.6
	return v
	
#++++++++++velocidadMedia+++++++++++++++
#Una bici va a 5m/s durante 5 minutos y luego cambia a una velocidad media de 8 m/s durante los siguientes 10 minutos. 
#Cuantos km habra recorrido en total? Cual es la velocidad media (m/s) de todo el recorrido?

def velm_datos():
	lista=[]
	v1=randint(4,6)
	v2=randint(6,10)
	t1=randint(3,6)
	t2=randint(10,20)
	lista.extend([v1,v2,t1,t2])
	return lista
	
def velm(lista):
	d=lista[0]*lista[2]*60+lista[1]*lista[3]*60
	vm=float(d)/(lista[2]*60+lista[3]*60)
	return (d,vm)
 
 
#++++++++++Valor minimo mu++++++++++++++
#Caemos por una montanya de ALPHA grados de inclinacion en un trineo sobre hielo, lo que nos deja casi sin rozamiento,
#en un primer tramo de X1 metros, a partir de ese momento, la superficie se convierte en nieve dura y ofrece rozamiento; por
#suerte, porque vamos en el trineo sin saber frenarlo. Que minimo coeficiente de rozamiento ha de tener el suelo en el segundo tramo
#para que no caigamos por el precipicio que hay al final de la montanya si desde el principio del descenso al final hay X metros.


def mumin_datos():
	lista=[]
	alpha=randint(10,70)
	x=randint(50,100)
	x1=randint(10,20)
	lista.extend([alpha,x,x1])
	return lista

def mumin(lista):
	lista[0]=float(lista[0])
	lista[1]=float(lista[1])
	lista[2]=float(lista[2])
	mu=math.tan(math.radians(lista[0]))*((lista[2]/(lista[1]-lista[2]))+1)
	return mu
	
 
#++++++++++Rozamiento agua++++++++++++++

 
#+++++++++++++++caida libro con folio concepto rozamiento+++++++++++

#+++++++++++velocidad limite gota agua++++++++++++++++++++
#El rozamiento dinamico se da cuando un cuerpo se mueve dentro de un fluido, y su efecto depende, entre otras cosas, 
#de la superficie del cuerpo en cuestion, la densidad del medio y la velocidad relativa entre el cuerpo y el medio.
#El coeficiente de este rozamiento en el caso de una esfera en el aire es 3.4times10-4r kg/s, donde r esta en metros. 
#Cual es la velocidad limite que puede conseguir una gota de agua de 0.5 mm de radio al caer al suelo?

def gota_datos():
	lista=[]
	diam=random.uniform(0.1,2.0)
	diam=round(diam,2)
	lista.append(diam)
	return lista
	
def gota(lista):
	r=lista[0]/1000
	gamma=3.4*(10**(-4))*r
	densidad=1000.0
	masa=densidad*(4.0/3.0)*math.pi*r**3
	v=masa*constantes.G/gamma
	return v


# Prueba Willy
def cine1_datos():
	lista=[]
	diam=random.uniform(0.1,2.0)
	diam=round(diam,2)
	lista.append(diam)
	return lista

def cine1_solucion(lista):
	r=lista[0]/1000
	return r

 
 
 







