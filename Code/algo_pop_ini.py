#!/usr/bin/python3
# -*-coding:Utf-8 -*

import numpy as np
from heapq import heappush, heappop, nsmallest #gere les files de priorite avec un arbre binaire.
import itertools
import random
import sys
sys.path.append("../Donnees")
from calcul_cout import *
from TreeStruct import *
from fil_priorite import *
import copy
from time import time


def algoPrimAlea1(n_num, n, tab_sommets, tab_cout1, tab_cout2, n_proche):
	"""docstring for algoPrimAlea1 :
		n_num : Numéro de l'arbre généré dans la génération
		n : Nombre de sommets de l'arbre
		tab_sommets : tableau des sommets que l'on prend
		tab_cout1 : tableau de cout des sommets"""

	#implementation d'une file de priorite. L'acces de se fait en log(n)
	pq = Fil_prio([],{},itertools.count())                         # list of entries arranged in a heap
	#Initialisation
	h = [-1]*(n+1) #h(v) renvoie le sommet dont le cout avec v est minimal
	b = [False]*(n+1) # b(v) indique si le sommet v est dans l'arbre
	c = [9999999]*(n+1) # c(v) est le cout qui correspond aux b(v). On initialise à l'infini

	#La solution de l'arbre est stocke dans un arbre parent :
	tree = [0]*(n + 1)
	
	###### Algo de Prim #######
	#La racine est prise au hasard.
	tab_indice = range(1,n + 1)
	#i_hmin = random.randint(1,n) #indice du hmin choisi. Prend un entier entre 0 et n inclu.
	i_hmin = 1
	hmin = tab_sommets[i_hmin]
	tree[i_hmin] = i_hmin
	b[i_hmin] = True

	for k in range(1,n):
		i_hder = i_hmin
		#Si on veut seulement mettre à jour dans un certain rayon. Finalement on perd du temps à le faire.
		#for i in [l for l in tab_indice if (b[l] == False and (h[l] == -1 or getcout(tab_cout1,tab_sommets[l],tab_sommets[i_hder]) < R))]:
		for i in [l for l in tab_indice if b[l] == False]:
			if h[i] == -1 or getcout(tab_cout1,tab_sommets[i],tab_sommets[i_hder]) < getcout(tab_cout1,tab_sommets[i],tab_sommets[h[i]]): #Si on avait pas encore vu ce sommet au moins une fois, il faut rentrer dans cette condition.
				h[i] = i_hder
				c[i] = getcout(tab_cout1,tab_sommets[i],tab_sommets[h[i]])
				pq.add_task(i,c[i])
		#On va choisir quel sommet choisir dans un rayon donné.
		if n - k < n_proche:
			n_proche = n-k
		#Trop lent de faire comme ci-dessous
		#tab = sorted(pq, key=lambda tuple: [260,0,0] if tuple[2] is REMOVED else tuple)[:n_proche]
		#Ce n'est pas totalement les n plus proches mais ça passe
		tab = [x for x in pq.fil if x[2] is not pq.REMOVED][:n_proche]
		#tab = nsmallest(n_proche, pq.fil, key=lambda tuple: [260,0,0] if tuple[2] is REMOVED else tuple)

		i_hmin = random.choice(tab)[2]
		pq.add_task(i_hmin,0)
		i_hmin = pq.pop_task()
		b[i_hmin] = True
		tree[i_hmin] = h[i_hmin]

	return TreeStruct(n, 1, n_num, tree, tab_cout1, tab_cout2, tab_sommets)


def algoPrimAlea2(n_num, n, tab_sommets, tab_cout1, tab_cout2, n_proche):
	"""docstring for algoPrimAlea2 :
		n_num : Numéro de l'arbre généré dans la génération
		n : Nombre de sommets de l'arbre
		tab_sommets : tableau des sommets que l'on prend
		tab_cout1 : tableau de cout des sommets
		n_proche : On regarde les n_proche meilleurs noeuds et non pas le meilleurs noeud"""

	#implementation d'une file de priorite. L'acces de se fait en log(n)
	pq = Fil_prio([],{},itertools.count())
	#Initialisation
	h = [-1]*(n+1) #h(v) renvoie le sommet dont le cout avec v est minimal
	b = [False]*(n+1) # b(v) indique si le sommet v est dans l'arbre
	c = [9999999]*(n+1) # c(v) est le cout qui correspond aux b(v). On initialise à l'infini

	#La solution de l'arbre est stocke dans un arbre parent :
	tree = [0]*(n + 1)
	
	###### Algo de Prim #######
	#La racine est prise au hasard.
	tab_indice = range(1,n + 1)
	i_hmin = 1
	hmin = tab_sommets[i_hmin]
	tree[i_hmin] = i_hmin
	b[i_hmin] = True
	total = 0
	for k in range(1,n):
		i_hder = i_hmin
		#Si on veut seulement mettre à jour dans un certain rayon. Finalement on perd du temps à le faire.
		#for i in [l for l in tab_indice if (b[l] == False and (h[l] == -1 or getcout(tab_cout1,tab_sommets[l],tab_sommets[i_hder]) < R))]:
		
		for i in [l for l in tab_indice if b[l] == False]:
			if h[i] == -1 or getcout(tab_cout1,tab_sommets[i],tab_sommets[i_hder]) < getcout(tab_cout1,tab_sommets[i],tab_sommets[h[i]]): #Si on avait pas encore vu ce sommet au moins une fois, il faut rentrer dans cette condition.
				h[i] = i_hder
				c[i] = getcout(tab_cout1,tab_sommets[i],tab_sommets[h[i]])
				pq.add_task(i,c[i])
		
		
		#On va choisir quel sommet choisir dans un rayon donné.
		
		if n - k < n_proche:
			n_proche = n-k

		pq_temp = Fil_prio(pq.fil[:],pq.entry_finder.copy(),copy.copy(pq.counter))

		tab = []
		#On fait en fait un petit heapsort sur une copie de notre fil de priorité.
		for i in range(n_proche):
			tab.append(pq_temp.pop_task())

		i_hmin = random.choice(tab)
		#On met en prioritaire le sommet choisi
		pq.add_task(i_hmin,0)
		#Puis on l'enlève.
		i_hmin = pq.pop_task()

		b[i_hmin] = True
		tree[i_hmin] = h[i_hmin]
	
	return TreeStruct(n, 1, n_num, tree,tab_cout1, tab_cout2, tab_sommets)

def algoPrimAlea3(n_num, n, tab_sommets, tab_cout1, tab_cout2, n_proche):
	"""docstring for algoPrimAlea2 :
		n_num : Numéro de l'arbre généré dans la génération
		n : Nombre de sommets de l'arbre
		tab_sommets : tableau des sommets que l'on prend
		tab_cout1 : tableau de cout des sommets
		n_proche : On regarde les n_proche meilleurs noeuds et non pas le meilleurs noeud"""

	#Procédure qui ajoute au élément dans un tableau trié
	def ajouter(x,a,a_indice,sommet,len_max) :
		i = 0 ; j = len(a)
		while j>i :
			k = (i+j)//2
			if x < a[k] :  j = k
			else :  i = (k+1)
		a.insert(i,x)
		a_indice.insert(i,sommet)
		if len(a) > len_max:
			a.pop()
			a_indice.pop()


	#Initialisation
	h = [-1]*(n+1) #h(v) renvoie le sommet dont le cout avec v est minimal
	b = [False]*(n+1) # b(v) indique si le sommet v est dans l'arbre
	c = [9999999]*(n+1) # c(v) est le cout qui correspond aux b(v). On initialise à l'infini

	#La solution de l'arbre est stocke dans un arbre parent :
	tree = [0]*(n + 1)
	
	###### Algo de Prim #######
	tab_indice = range(1,n + 1)
	i_hmin = 1
	hmin = tab_sommets[i_hmin]
	tree[i_hmin] = i_hmin
	b[i_hmin] = True
	total = 0
	for k in range(1,n):
		i_hder = i_hmin
		tab_cmin = [9999999]
		tab_imin = [9999999]
		#Si on veut seulement mettre à jour dans un certain rayon. Finalement on perd du temps à le faire.
		#for i in [l for l in tab_indice if (b[l] == False and (h[l] == -1 or getcout(tab_cout1,tab_sommets[l],tab_sommets[i_hder]) < R))]:
		
		if n - k < n_proche:
			n_proche = n-k

		for i in [l for l in tab_indice if b[l] == False]:
				if h[i] == -1 or getcout(tab_cout1,tab_sommets[i],tab_sommets[i_hder]) < getcout(tab_cout1,tab_sommets[i],tab_sommets[h[i]]): #Si on avait pas encore vu ce sommet au moins une fois, il faut rentrer dans cette condition.
					h[i] = i_hder
					c[i] = getcout(tab_cout1,tab_sommets[i],tab_sommets[h[i]])
				if c[i] < tab_cmin[-1]:
					ajouter(c[i], tab_cmin, tab_imin,i, n_proche)

		i_hmin = random.choice(tab_imin)

		b[i_hmin] = True
		tree[i_hmin] = h[i_hmin]
	
	return TreeStruct(n, 1, n_num, tree,tab_cout1, tab_cout2, tab_sommets)



def algoPrim(n_num, n, tab_sommets, tab_cout1, tab_cout2):
	"""docstring for algoPrimAlea2 :
		n_num : Numéro de l'arbre généré dans la génération
		n : Nombre de sommets de l'arbre
		tab_sommets : tableau des sommets que l'on prend
		tab_cout1 : tableau de cout des sommets"""

	pq = Fil_prio([],{},itertools.count())

	#Initialisation
	h = [-1]*(n+1) #h(v) renvoie le sommet dont le cout avec v est minimal
	b = [False]*(n+1) # b(v) indique si le sommet v est dans l'arbre
	c = [9999999]*(n+1) # c(v) est le cout qui correspond aux b(v). On initialise à l'infini

	#La solution de l'arbre est stocke dans un arbre parent :
	tree = [0]*(n + 1)
	
	###### Algo de Prim #######
	#La racine est prise au hasard.
	tab_indice = range(1,n + 1)
	i_hmin = 1
	hmin = tab_sommets[i_hmin]
	tree[i_hmin] = i_hmin
	b[i_hmin] = True

	for k in range(1,n):
		i_hder = i_hmin
		for i in [l for l in tab_indice if b[l] == False]:
			if h[i] == -1 or getcout(tab_cout1,tab_sommets[i],tab_sommets[i_hder]) < getcout(tab_cout1,tab_sommets[i],tab_sommets[h[i]]): #Si on avait pas encore vu ce sommet au moins une fois, il faut rentrer dans cette condition.
				h[i] = i_hder
				c[i] = getcout(tab_cout1,tab_sommets[i],tab_sommets[h[i]])
				pq.add_task(i,c[i])

		i_hmin = pq.pop_task()
		b[i_hmin] = True
		tree[i_hmin] = h[i_hmin]

	return TreeStruct(n, 1, n_num, tree,tab_cout1, tab_cout2, tab_sommets)
