#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import numpy as np
import pickle
import sys
sys.path.append("../Donnees")
sys.path.append("../Dessin_graphe")
from selection_donnees import *
from dessine_graphe import *

from algo_pop_ini import *

class AlgoGenetique(object):
	"""docstring for TreeStruct:
	Cette classe correspond a un algo genetique.
	Il faut beaucoup de parametre pour definir cet algo.
	- nb_population_initial : taille de la population initiale
	- nb_population : taille de la population après Selection
	- generation sa génération
	- numero le numéro de l'arbre
	- tree le tableau de structure"""
	def __init__(self,taillePopIni,MpopInitial,taillePop):
		self.taillePop = taillePop #Nombre d'individu par génération 
		self.taillePopIni = taillePopIni # Taille de la population initiale.
		self.MpopInitial = MpopInitial # String qui indique quelle méthode utilisée pour la génération de la population initiale.
		self.tab_population = [] # Initialement vide, il faudra le remplir une première fois avec la méthode de génération initiale.
		self.numGeneration = 1 # Numéro de la génération courante.

	def generePopInitiale(self,tab_sommets,tab_cout1):
		if self.taillePopIni < self.taillePop:
			print("Warning : taillePopIni < taillePop\nOn pose taillePopIni = taillePop")
			self.taillePopIni = self.taillePop
		if self.MpopInitial == "Prime1":
			for i in range(self.taillePopIni):
				self.tab_population.append(algoPrimeAlea(tab_sommets,tab_cout1))
		else:
			print("Erreur : MpopInitial non reconnue")


if __name__ == "__main__":

	nb_sommet = 100

	with open('../Donnees/tab_cout1', 'rb') as fichier:
		mon_depickler = pickle.Unpickler(fichier)
		tab_cout1 = mon_depickler.load()

	with open('../Donnees/tab_coord', 'rb') as fichier:
		mon_depickler = pickle.Unpickler(fichier)
		tab_coord = mon_depickler.load()
		nb_sommet_total = mon_depickler.load()

	tab_sommets = select_sample(nb_sommet_total,nb_sommet)


	testAlgo = AlgoGenetique(40, "Prime1", 20)
	testAlgo.generePopInitiale(tab_sommets, tab_cout1)
	print(testAlgo.tab_population)