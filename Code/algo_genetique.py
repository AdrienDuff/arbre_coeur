#!/usr/local/bin/python3.5
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
from algo_croisement import *
from resolution_exacte import *
import plotly.plotly as py
import plotly.graph_objs as go

def ajouter_individu(Tree,tab) :
		i = 0 ; j = len(tab)
		while j>i :
			k = (i+j)//2
			if Tree.cout < tab[k].cout :  j = k
			else :  i = (k+1)
		tab.insert(i,Tree)


class AlgoGenetique(object):
	"""docstring for AlgoGenetique:
	Cette classe correspond a un algo genetique.
	Il faut beaucoup de parametre pour definir cet algo.
	- nb_population_initial : taille de la population initiale
	- nb_population : taille de la population après Selection
	- generation sa génération
	- numero le numéro de l'arbre
	- tree le tableau de structure"""
	def __init__(self,taillePop,MpopInitial, Mselection, Mcroisement, Mmutation, tab_cout1, tab_cout2, tab_coord,tab_sommets, nb_sommet,n_proche,nb_chemin,longeur_chemin_max, nb_generation, rayon_mut, proba_mut):
		#self.taillePop = taillePop #Nombre d'individu par génération 
		self.taillePop = taillePop # Taille de la population initiale.
		self.MpopInitial = MpopInitial # String qui indique quelle méthode utilisée pour la génération de la population initiale.
		self.Mcroisement = Mcroisement # String qui indique quelle méthode utilisée pour le croisement de deux individus.
		self.Mmutation = Mmutation # String qui indique quelle méthode utilisée pour la mutation des enfants.
		self.Mselection = Mselection # String qui indique quelle méthode utilisée pour la sélection.
		self.tab_population = [] # Initialement vide, il faudra le remplir une première fois avec la méthode de génération initiale.
		self.newPop = [] # Sert à stocker les enfants produits
		self.numGeneration = 1 # Numéro de la génération courante.
		self.tab_cout1 = tab_cout1 #les données
		self.tab_cout2 = tab_cout2
		self.tab_coord = tab_coord
		self.tab_sommets = tab_sommets # La liste de tout les sommets utilisés
		self.nb_sommet = nb_sommet #Le nombre de sommet des arbres couvrants
		self.n_proche = n_proche # On regarde les n plus proche voisin lors de l'algo de primAlea
		self.nb_chemin = nb_chemin # le nombre de chemin à échanger pour générer des enfants
		self.longeur_chemin_max = longeur_chemin_max
		self.bestTree = 0 #On stocke ici le meilleurs arbre jamais trouvé
		self.nbGeneration = nb_generation
		self.evolution_cout = []
		self.Tree_Cplex = 0 #Sert au stockage de l'arbre calculé par Cplex si cela est demandé
		self.genere_poids()
		self.rayon_mut = rayon_mut
		self.proba_mut = proba_mut

	def genere_poids(self):
		tab = []
		for i in range(1,taillePop):
			tab.extend([i]*(int((3/2)*i)))
		self.indice_weighted = tab

	def generePopInitiale(self, dessin = False, countTime = False):
		"""docstring for generePopInitiale
		n_proche : Sert à choisir aléatoirement un sommet à ajouter dans ce rayon de proche voisin.
		"""
		#Les arbres sont classés dans l'ordre décroissant.
		"""
		if self.taillePop < self.taillePop:
			print("Warning : taillePop < taillePop\nOn pose taillePop = taillePop")
			self.taillePop = self.taillePop
		"""

		if self.MpopInitial == "primAlea1":
			self.tab_population = []
			for i in range(1,self.taillePop):
				start_time = time()
				individu = algoPrimAlea1(i, self.nb_sommet, self.tab_sommets,self.tab_cout1,self.tab_cout2,self.n_proche)
				individu.calcul_cout()
				ajouter_individu(individu, self.tab_population)
				end_time = time()
				if dessin:
					individu.dessine_toi(self.tab_sommets, self.tab_coord)
				if countTime:
					print(end_time - start_time)
			#On ajoute selui avec prim
			start_time = time()
			individu = algoPrim(i, self.nb_sommet, self.tab_sommets,self.tab_cout1,self.tab_cout2)
			individu.calcul_cout()
			ajouter_individu(individu, self.tab_population)
			end_time = time()
			if dessin:
					individu.dessine_toi(self.tab_sommets, self.tab_coord)
			if countTime:
					print(end_time - start_time)

			self.tab_population.reverse()
			self.bestTree = self.tab_population[-1]
			self.evolution_cout.append(self.bestTree.cout)

		elif self.MpopInitial == "primAlea2":
			self.tab_population = []
			for i in range(1,self.taillePop):
				start_time = time()
				individu = algoPrimAlea2(i, self.nb_sommet, self.tab_sommets,self.tab_cout1,self.tab_cout2,self.n_proche)
				individu.calcul_cout()
				ajouter_individu(individu, self.tab_population)
				end_time = time()
				if dessin:
					individu.dessine_toi(self.tab_sommets, self.tab_coord)
				if countTime:
					print(end_time - start_time)

			#On ajoute selui avec prim
			start_time = time()
			individu = algoPrim(i, self.nb_sommet, self.tab_sommets,self.tab_cout1,self.tab_cout2)
			individu.calcul_cout()
			ajouter_individu(individu, self.tab_population)
			end_time = time()
			if dessin:
					individu.dessine_toi(self.tab_sommets, self.tab_coord)
			if countTime:
					print(end_time - start_time)

			self.tab_population.reverse()
			self.bestTree = self.tab_population[-1]
			self.evolution_cout.append(self.bestTree.cout)

		elif self.MpopInitial == "primAlea3":
			self.tab_population = []
			for i in range(1,self.taillePop +1):
				start_time = time()
				individu = algoPrimAlea3(i, self.nb_sommet, self.tab_sommets,self.tab_cout1,self.tab_cout2,self.n_proche)
				individu.calcul_cout()
				ajouter_individu(individu, self.tab_population)
				end_time = time()
				if countTime:
					print(end_time - start_time)
			#On ajoute selui avec prim
			start_time = time()
			individu = algoPrim(i, self.nb_sommet, self.tab_sommets,self.tab_cout1,self.tab_cout2)
			individu.calcul_cout()
			ajouter_individu(individu, self.tab_population)
			end_time = time()

			if countTime:
					print(end_time - start_time)

			if dessin:
				for i in range(len(self.tab_population)):
					self.tab_population[i].dessine_toi(self.tab_sommets, self.tab_coord)
			self.tab_population.reverse()
			self.bestTree = self.tab_population[-1]
			self.evolution_cout.append(self.bestTree.cout)

		elif self.MpopInitial == "prim":
			self.tab_population = []
			for i in range(1,self.taillePop +1):
				start_time = time()
				individu = algoPrim(i, self.nb_sommet, self.tab_sommets,self.tab_cout1,self.tab_cout2)
				individu.calcul_cout()
				ajouter_individu(individu, self.tab_population)
				end_time = time()
				if dessin:
					individu.dessine_toi(self.tab_sommets, self.tab_coord)
				if countTime:
					print(end_time - start_time)
			self.tab_population.reverse()
			self.bestTree = self.tab_population[-1]
			self.evolution_cout.append(self.bestTree.cout)

		else:
			print("Erreur : MpopInitial non reconnue")

	def select2Tree(self):
		"""La probabilité de sélection se fait de manière proportionnelle à sa place dans le tableau de population
			qui est classé dans l'ordre décroissant. Le 1er ne peut jamais être pris et le meilleurs a une chance sur deux d'être choisie.
		"""
		#Il y a de moins en moins de chance de choisir un arbre déjà choisi
		indice1 = random.choice(self.indice_weighted)
		self.indice_weighted.remove(indice1)
		tmp = [x for x in self.indice_weighted if x != indice1]
		indice2 = random.choice(tmp)
		self.indice_weighted.remove(indice2)
		return [self.tab_population[indice1],self.tab_population[indice2]]

	def croisement2Arbre(self, Arbre1, Arbre2, num_Arbre, dessin = False, countTime = False):
		start_time = time()
		if self.Mcroisement == "croisement1":
			Arbre_enfants = algo2Enfants_1(self.nb_sommet,Arbre1,Arbre2, num_Arbre, self.nb_chemin, self.longeur_chemin_max, self.numGeneration)
		end_time = time()

		if countTime:
			print(end_time - start_time)
		if dessin:
			Arbre_enfants[0].dessine_toi(self.tab_sommets, self.tab_coord)
			Arbre_enfants[1].dessine_toi(self.tab_sommets, self.tab_coord)
		return Arbre_enfants

	def croisementAll(self,dessin = False, countTime = False):
		newPop = []
		if self.Mselection == "selection1":
			num_Arbre = 1
			for i in range(int(self.taillePop /2)):
				Arbres = self.select2Tree() # Les premiers individus sont peut être trop souvent choisie ?
				Enfants = self.croisement2Arbre(Arbres[0], Arbres[1],num_Arbre, dessin = dessin, countTime = countTime, )
				newPop.append(self.mutation(Enfants[0]))
				newPop.append(self.mutation(Enfants[1]))
				num_Arbre += 2
		#1/4 des arbres viennent des meilleurs de la génération précédente
		if self.Mselection == "selection2":
			nb_croisement = int(self.taillePop*(9/10))
			if nb_croisement % 2 == 1:
				nb_croisement = nb_croisement + 1
			num_Arbre = 1
			for i in range(int(nb_croisement /2)):
				Arbres = self.select2Tree() # Les premiers individus sont peut être trop souvent choisie ?
				Enfants = self.croisement2Arbre(Arbres[0], Arbres[1],num_Arbre,dessin = dessin, countTime = countTime)
				newPop.append(self.mutation(Enfants[0]))
				newPop.append(self.mutation(Enfants[1]))
				num_Arbre += 2
			nb_old = self.taillePop - nb_croisement
			newPop.extend(self.tab_population[-nb_old:])
		self.genere_poids()

		self.newPop = newPop
				
	def mutation(self, Arbre, countTime = False):
		start_time = time()
		if self.Mmutation == "mutation1":
			mutation = np.random.binomial(1, self.proba_mut)
			if mutation:
				valide = False
				while valide == False:
					i = random.choice(np.arange(1,self.nb_sommet+1))
					j = i
					while i == j:
						j = random.choice(np.arange(1,self.nb_sommet+1))
					if getcout(self.tab_cout1, tab_sommets[i], tab_sommets[j]) < self.rayon_mut:
						valide = True
				j_is_down_to_i = False
				if i == 1 : j_is_down_to_i = True
				current = j
				while current != 1 and j_is_down_to_i == False:
					current = Arbre.tree[current]
					if current == i : j_is_down_to_i = True
				if j_is_down_to_i:
					Arbre.tree[j] = i
				else:
					Arbre.tree[i] = j
			end_time = time()
		if countTime:
			print(end_time - start_time)
		return Arbre


	def nextGeneration(self):
		self.croisementAll() # Les enfants sont dans newPop
		self.tab_population = []
		for enfant in self.newPop:
			#self.mutation(enfant) 
			enfant.calcul_cout()
			ajouter_individu(enfant, self.tab_population)
		self.tab_population.reverse()
		if self.tab_population[-1].cout < self.bestTree.cout:
			self.bestTree = self.tab_population[-1]
		self.evolution_cout.append(self.bestTree.cout)
		self.numGeneration = self.numGeneration + 1


	def nextnGeneration(self,n):
		pas_mieux = 0
		old_cout = 0
		Stop = False
		i = 0
		while i < n and Stop == False:
			self.nextGeneration()
			if self.bestTree.cout != old_cout:
				old_cout = self.bestTree.cout
				pas_mieux = 0
			else:
				pas_mieux = pas_mieux + 1
			if pas_mieux >= 200: # Si cela fait 200 générations qu'il n'y a pas eu d'amélioration, on arrête.
				Stop = True
			i = i + 1
			sys.stdout.write("Génération " + str(self.numGeneration) + "/" +str(self.nbGeneration) + " crée !" + chr(13))
		print("")


	def lance_algo(self):
		self.nextnGeneration(self.nbGeneration - 1)

	def solve_with_cplex(self):
		self.Tree_Cplex = resolution_cplex(self.nb_sommet, self.tab_sommets,self.tab_cout1,self.tab_cout2)

	def dessine_evolution_cout(self, name = ""):
		trace0 = go.Scatter(
				x = np.arange(1,len(self.evolution_cout)+1),
				y = self.evolution_cout,
				mode = 'lines+markers',
				name = 'Evolution du meilleurs cout à chaque génération'
				)
		data = [trace0]

		if self.Tree_Cplex != 0 and self.Tree_Cplex != -1:
			trace1 = go.Scatter(
				x = np.arange(1,len(self.evolution_cout)+1),
				y = [self.Tree_Cplex.cout]*len(self.evolution_cout),
				mode = 'lines',
				name = "Cout de l'arbre calculé par CPLEX"
				)
			data.append(trace1)


		plotly.offline.plot(data, filename='evolution_cout' + name + '.html')
		#py.iplot(data, filename='evolution_cout')




if __name__ == "__main__":

	nb_sommet = 500

	n_proche = 160 # pour algo primAlea

	nb_chemin = 5 # pour algo de croisement
	longeur_chemin_max = 10

	taillePop = 40 # IL faut un nombre pair
	nb_generation = 2000

	rayon_mut = 120 #Rayon de mutation possible
	proba_mut = 0.3
	methode_ini = "primAlea3"
	#methode_ini = "prim"
	methode_selection = "selection2"
	methode_croisement = "croisement1"
	methode_mutation = "mutation1"

	print("Chargement des données...")
	with open('../Donnees/tab2_cout1', 'rb') as fichier:
		mon_depickler = pickle.Unpickler(fichier)
		tab_cout1 = mon_depickler.load()

	with open('../Donnees/tab2_cout2', 'rb') as fichier:
		mon_depickler = pickle.Unpickler(fichier)
		tab_cout2 = mon_depickler.load()

	with open('../Donnees/tab2_coord', 'rb') as fichier:
		mon_depickler = pickle.Unpickler(fichier)
		tab_coord = mon_depickler.load()
		nb_sommet_total = mon_depickler.load()
	print("Fait")

	tab_sommets = select_sample(nb_sommet_total,nb_sommet)

	testAlgo = AlgoGenetique(taillePop, methode_ini,methode_selection, methode_croisement, methode_mutation, tab_cout1, tab_cout2, tab_coord, tab_sommets,nb_sommet,n_proche, nb_chemin, longeur_chemin_max, nb_generation , rayon_mut, proba_mut)

	print("Génération population initiale...")
	testAlgo.generePopInitiale(dessin = False, countTime = True)
	#testAlgo2 = copy.deepcopy(testAlgo)

	#testAlgo2.Mselection = "selection2"
	#testAlgo2.MpopInitial = "prim"
	#testAlgo2.generePopInitiale(dessin = False)
	#testAlgo2.tab_population[-1].numGeneration =-1
	#testAlgo2.tab_population[-1].dessine_toi(tab_sommets, tab_coord)
	#arbres = testAlgo.select2Tree()
	print("croisement")
	#testAlgo.croisement(arbres[0], arbres[1], dessin = True, countTime = True)
	#testAlgo.croisementAll(countTime = True)
	#testAlgo.nextnGeneration(10)
	
	#testAlgo.solve_with_cplex()
	#testAlgo.Tree_Cplex.calcul_cout()
	#testAlgo.Tree_Cplex.dessine_toi(tab_sommets, tab_coord)


	testAlgo.lance_algo()
	print("Fait")
	testAlgo.dessine_evolution_cout("1")
	testAlgo.bestTree.dessine_toi(tab_sommets, tab_coord)

	#testAlgo2.lance_algo()
	#testAlgo2.dessine_evolution_cout("2")
	#testAlgo.bestTree.dessine_toi(tab_sommets, tab_coord)
	#testAlgo.Tree_Cplex.dessine_toi(tab_sommets, tab_coord)
	#print(testAlgo.evolution_cout)
	#testAlgo.select2Tree()

	#testAlgo.solve_with_cplex()
	#testAlgo.Tree_Cplex.calcul_cout()
	#testAlgo.Tree_Cplex.dessine_toi(tab_sommets, tab_coord)

	#for arbre in testAlgo.tab_population:
	#   arbre.dessine_toi(tab_sommets, tab_coord)
	#testAlgo.tab_population[1].dessine_toi(tab_sommets, tab_coord)
