#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import numpy as np
import csv
import pickle

csv_coord = csv.reader(open("coordonnees_x_y.csv","r"))

np_coord = np.array([[0,0,0]], float)
nb_sommet = 0
#Transformation du csv en un tableau numpy qui est facile d'utilisation
for row in csv_coord:
	nb_sommet = nb_sommet + 1
	tab = [[nb_sommet,float(row[1]),float(row[2])]]
	np_coord = np.concatenate((np_coord, tab),axis=0)
	print(nb_sommet)

#On enregistre le tableau numpy dans un fichier.
with open('tab_coord', 'wb') as fichier:
	mon_pickler = pickle.Pickler(fichier)
	mon_pickler.dump(np_coord)
	mon_pickler.dump(nb_sommet)
