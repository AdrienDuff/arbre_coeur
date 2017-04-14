#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import numpy as np
import pickle
import math

with open('tab_coord', 'rb') as fichier:
	mon_depickler = pickle.Unpickler(fichier)
	tab_coord = mon_depickler.load()
	nb_sommet = mon_depickler.load()

def distance(sommet1,sommet2):
	"Calcul la distance en kilomètre entre deux sommets"
	x1 = tab_coord[sommet1][1]
	y1 = tab_coord[sommet1][2]
	x2 = tab_coord[sommet2][1]
	y2 = tab_coord[sommet2][2]
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def cout1(sommet1,sommet2):
	return distance(sommet1,sommet2)

def cout2(sommet1,sommet2):
	return distance(sommet1,sommet2)/2