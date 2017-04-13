#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import csv
from math import *

c_old = csv.reader(open("codesinseecommunesgeolocalisees.csv","r"))

c_new = csv.writer(open("coordonnees_x_y.csv", "w"))

i = 0
x_max = 0
y_max = 0
x_min = 10000000000000000
y_min = 10000000000000000

#Constantes de projection de Lambert France. Lambert I.
#Transformation des coordonnees gerographiques phi, lambda en coordonnees de Lambert x et y.
#http://geodesie.ign.fr/contenu/fichiers/documentation/pedagogiques/TransformationsCoordonneesGeodesiques.pdf
n = 0.7604059656
C = 11603796.98
Xs = 600000.000
Ys = 5657616.674
l0 = 0
e = 0.08248325676

for row_old in c_old:
	#On enleve la premiere ligne qui nous interesse pas
	if i != 0:
		#On garde le num INSEE
		row_new = [row_old[0]]
		c_lambda = float(row_old[4])
		c_phi = float(row_old[5])

		isometrique = (1/2)*log((1 + sin(c_phi))/(1 - sin(c_phi))) - (e/2)*log((1 + e*sin(c_phi))/(1-e*sin(c_phi)))
		R = C*exp(-n*isometrique)
		c_gamma = n*(c_lambda - l0)

		x = Xs + R*sin(c_gamma)
		y = Ys - R*cos(c_gamma)

		#On convertie en km et on centre sur Paris
		x = (x - 772094.2929622594)/1000
		y = (y - 131598.89387428667)/1000
		#On calcul les min et max pour voir ce que cela donne
		if x>x_max:
			x_max = x
		if x< x_min:
			x_min = x
		if y > y_max:
			y_max = y
		if y < y_min:
			y_min =y

		row_new.append(x)
		row_new.append(y)
		c_new.writerow(row_new)
	i = i + 1


print(x_min,x_max)
print(y_min,y_max)