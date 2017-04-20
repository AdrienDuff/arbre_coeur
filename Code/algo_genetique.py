#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import numpy as np
import pickle
import sys
sys.path.append("../Donnees")
sys.path.append("../Dessin_graphe")
from selection_donnees import *
from dessine_graphe import *
from time import time
from algo_pop_ini import *

class AlgoGenetique(object):
	"""docstring for AlgoGenetique:
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


	def generePopInitiale(self, nb_sommet, tab_sommets, tab_coord, tab_cout1, n_proche = 15, dessin = False, countTime = False):
		"""docstring for generePopInitiale
		n_proche : Sert à choisir aléatoirement un sommet à ajouter dans ce rayon de proche voisin.
		"""
		if self.taillePopIni < self.taillePop:
			print("Warning : taillePopIni < taillePop\nOn pose taillePopIni = taillePop")
			self.taillePopIni = self.taillePop

		if self.MpopInitial == "primAlea1":
			self.tab_population = []
			for i in range(1,self.taillePopIni +1):
				start_time = time()
				self.tab_population.append(algoPrimAlea1(i, nb_sommet, tab_sommets,tab_cout1,n_proche))
				end_time = time()
				if dessin:
					self.tab_population[-1].dessine_toi(tab_sommets, tab_coord)
				if countTime:
					print(end_time - start_time)

		elif self.MpopInitial == "primAlea2":
			self.tab_population = []
			for i in range(1,self.taillePopIni +1):
				start_time = time()
				self.tab_population.append(algoPrimAlea2(i, nb_sommet, tab_sommets,tab_cout1,n_proche))
				end_time = time()
				if dessin:
					self.tab_population[-1].dessine_toi(tab_sommets, tab_coord)
				if countTime:
					print(end_time - start_time)

		elif self.MpopInitial == "prim":
			self.tab_population = []
			for i in range(1,self.taillePopIni +1):
				start_time = time()
				self.tab_population.append(algoPrim(i, nb_sommet, tab_sommets,tab_cout1))
				end_time = time()
				if dessin:
					self.tab_population[-1].dessine_toi(tab_sommets, tab_coord)
				if countTime:
					print(end_time - start_time)
		else:
			print("Erreur : MpopInitial non reconnue")


if __name__ == "__main__":

	nb_sommet = 2000
	n_proche = 30
	with open('../Donnees/tab_cout1', 'rb') as fichier:
		mon_depickler = pickle.Unpickler(fichier)
		tab_cout1 = mon_depickler.load()

	with open('../Donnees/tab_coord', 'rb') as fichier:
		mon_depickler = pickle.Unpickler(fichier)
		tab_coord = mon_depickler.load()
		nb_sommet_total = mon_depickler.load()

	tab_sommets = select_sample(nb_sommet_total,nb_sommet)

	testAlgo = AlgoGenetique(3, "primAlea2", 3)
	testAlgo.generePopInitiale(nb_sommet,tab_sommets, tab_coord, tab_cout1,n_proche = n_proche, dessin = True, countTime = True)

	#for arbre in testAlgo.tab_population:
	#	arbre.dessine_toi(tab_sommets, tab_coord)
	#testAlgo.tab_population[1].dessine_toi(tab_sommets, tab_coord)
