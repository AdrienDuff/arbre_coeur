#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import numpy as np
import pickle
import math
from scipy import sparse

with open('tab_coord', 'rb') as fichier:
	mon_depickler = pickle.Unpickler(fichier)
	tab_coord = mon_depickler.load()
	nb_sommet_total = mon_depickler.load()

def distance(sommet1,sommet2):
	"Calcul la distance en kilomètre entre deux sommets"
	x1 = tab_coord[sommet1][1]
	y1 = tab_coord[sommet1][2]
	x2 = tab_coord[sommet2][1]
	y2 = tab_coord[sommet2][2]
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def calcul_cout1(sommet1,sommet2):
	c = int(distance(sommet1,sommet2))
	if (c == 0):
		c = 1
	elif (c>255):
		c = 255
	return c

def calcul_cout2(sommet1,sommet2):
	c = int(distance(sommet1,sommet2)*2)
	if (c == 0):
		c = 2
	elif (c>255):
		c = 255
	return c

def getcout(tab_cout,sommet1,sommet2):
	if (sommet1<sommet2):
		(sommet1,sommet2) = (sommet2,sommet1)
	indice = int((sommet1 - 2)*(sommet1 - 1)/2 + sommet2 - 1)
	return tab_cout[indice]

def setcout(tab_cout,sommet1,sommet2,valeur):
	if sommet1 < sommet2:
		(sommet1,sommet2) = (sommet2,sommet1)
	indice = int((sommet1 - 2)*(sommet1 - 1)/2 + sommet2 - 1)
	tab_cout[indice] = valeur

#tab_cout1 = np.zeros((nb_sommet_total + 1, nb_sommet_total +1),dtype=np.uint8)

#On utilise un tableau à une dimension pour stocker seulement les bons coefficients.
#Les couts sont stockes sur 8 bytes pour que cela prenne moins de place
tab_cout1 = np.zeros(int((nb_sommet_total*(nb_sommet_total-1))/2), dtype = np.uint8)
tab_cout2 = np.zeros(int((nb_sommet_total*(nb_sommet_total-1))/2), dtype = np.uint8)

#On rempli la matrice triangulaire inferieur
for i in range(2, nb_sommet_total + 1):
	print(i)
	for j in range(1, i):
		setcout(tab_cout1, i, j, calcul_cout1(i,j))
		setcout(tab_cout2, i, j, calcul_cout2(i,j))


print("")
print(getcout(tab_cout1, 14, 2))
print(getcout(tab_cout1, 2, 14))


with open('tab_cout1', 'wb') as fichier:
	mon_pickler = pickle.Pickler(fichier)
	mon_pickler.dump(tab_cout1)

print("")
print(getcout(tab_cout2, 14, 2))
print(getcout(tab_cout2, 2, 14))

with open('tab_cout2', 'wb') as fichier:
	mon_pickler = pickle.Pickler(fichier)
	mon_pickler.dump(tab_cout2)