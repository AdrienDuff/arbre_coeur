#!/usr/bin/python3
# -*-coding:Utf-8 -*

import numpy as np
import random
from TreeStruct import *


def cheminAleatoire(tree, longeur_min = 2, longeur_max = 15):
	facteur = 10 # 10 fois plus de chance de continuer un chemin que de choisir une feuille
	chemin = []
	#On ne choisi pas une feuille donc on peut prendre comme début du chemin un sommet de tree.
	s = 1
	#Le while évite un cas pathologique
	while s == 1:
		s = random.choice(tree[2:])
	pred = s
	chemin.append(s)
	feuille = False

	#On choisi aléatoirement la taille du chemin entre 2 et n_sommet/2
	taille = random.randint(longeur_min, longeur_max)
	i = 1
	while i <= taille and feuille == False:
		choix = []
		#On ne peut pas rechoisir un sommet par lequel nous sommes déjà passé.
		#On ajoute le prédecesseur comme possibilité de chemin. La racine n'a pas de prédecesseur.
		if tree[s] != pred and s != 1:
			choix.extend([tree[s]]*facteur)
		#On ajoute les successeurs comme possibilité de chemin
		for indice,valeur in enumerate(tree[2:]):
			if valeur == s and (indice + 2) != pred:
				if (indice +2) in tree:
					choix.extend([indice+2]*facteur)
				else:
					choix.append(indice+2)
		pred = s
		#Si on n'a plus le choix, c'est que nous avons une feuille et la recherche d'un chemin s'arrete ici.)
		if len(choix) == 0:
			feuille = True
		else:
			s = random.choice(choix)
			chemin.append(s)
		i = i + 1
	return chemin



def genere1Enfant(tree, chemins):
	tree_enfant = tree[:]
	for chemin in chemins:
		for i in range(len(chemin)-1):
			found = False
			current = chemin[i]
			#Si le suivant est 1 alors il n'y a pas de doute sur qui est le parent de qui.
			if chemin[i+1] == 1:
				found = True
			while found == False and current != 1:
				if tree_enfant[current] == chemin[i+1]:
					#le sommet suivant est vers la racine
					found = True
				current = tree_enfant[current]

			#Si le suivant est plus haut dans l'arbre
			if found:
				tree_enfant[chemin[i]] = chemin[i+1]
			else:
				tree_enfant[chemin[i+1]] = chemin[i]
			i = i + 1
	return tree_enfant



def algo2Enfants_1(n, Arbre1, Arbre2, num_Arbre, nb_chemin, longeur_chemin_max, numGeneration):
	#Selection d'un Chemin aléatoire dans Arbre1
	chemins_arbre1 = []
	chemins_arbre2 = []
	tree1 = Arbre1.tree
	tree2 = Arbre2.tree
	#On génère le nombre de chemin qu'il faut
	for i in range(nb_chemin):
		chemins_arbre1.append(cheminAleatoire(tree1,longeur_max = longeur_chemin_max))
		chemins_arbre2.append(cheminAleatoire(tree2,longeur_max = longeur_chemin_max))


	tree_enfant1 = genere1Enfant(tree1, chemins_arbre2)
	tree_enfant2 = genere1Enfant(tree2, chemins_arbre1)

	Arbre_enfant1 = TreeStruct(n, numGeneration + 1, num_Arbre, tree_enfant1, Arbre1.tab_cout1, Arbre1.tab_cout2, Arbre1.tab_sommets)
	Arbre_enfant2 = TreeStruct(n, numGeneration + 1, num_Arbre + 1, tree_enfant2, Arbre2.tab_cout1, Arbre2.tab_cout2, Arbre2.tab_sommets)

	return [Arbre_enfant1,Arbre_enfant2]