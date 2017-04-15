#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import numpy as np
import pickle
import sys
sys.path.append("../Donnees")
sys.path.append("../Dessin_graphe")
from selection_donnees import *
from dessine_graphe import * 

with open('../Donnees/tab_coord', 'rb') as fichier:
	mon_depickler = pickle.Unpickler(fichier)
	tab_coord = mon_depickler.load()
	nb_sommet_total = mon_depickler.load()

with open('../Donnees/tab_cout1', 'rb') as fichier:
	mon_depickler = pickle.Unpickler(fichier)
	tab_cout1 = mon_depickler.load()

tab_sommets = select_sample(nb_sommet_total,100)

#dessine_graphe(tab_sommets, tab_coord)
