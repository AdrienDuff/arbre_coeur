#!/usr/local/bin/python3.5
# -*-coding:Utf-8 -

import cplex
from calcul_cout import *
from TreeStruct import *

my_obj = [1.0, 2.0, 3.0]
my_ub = [40.0, cplex.infinity, cplex.infinity]
my_colnames = ["x1", "x2", "x3"]
my_rhs = [20.0, 30.0]
my_rownames = ["c1", "c2"]
my_sense = "LL"

def populatebyrow(prob, tab_sommets, tab_cout1, tab_cout2):
	#On gagne du temps à mettre des indices au lieu de string comme nom de variables
	indice = 0
	str_ind = {}
	ind_str = {}
	racine = tab_sommets[1]
	print(racine)
	n = len(tab_sommets) - 1
	print(n)

	#Les 3 tableaux qui définissent la fonction objectif
	my_colnames = []
	types = []
	obj = []
	
	print("Fonction objective...")
	for i in tab_sommets[1:]:
		for j in tab_sommets[1:]:
			if j > i:
				obj.append(float(getcout(tab_cout1,i,j)))
				var = "x1_" + str(i) + "_" + str(j)
				str_ind[var] = indice
				ind_str[indice] = var
				my_colnames.append(var)
				indice = indice + 1
				types.append(prob.variables.type.binary)

				obj.append(float(getcout(tab_cout2,i,j)))
				var = "x2_" + str(i) + "_" + str(j)
				str_ind[var] = indice
				ind_str[indice] = var
				my_colnames.append(var)
				indice = indice + 1
				types.append(prob.variables.type.binary)

	
	for j in tab_sommets[2:]:
		i = racine
		if j < i:
			(i,j) = (j,i)
		obj.append(float(getcout(tab_cout1,i,j)))
		var = "x3_" + str(i) + "_" + str(j)
		str_ind[var] = indice
		ind_str[indice] = var
		my_colnames.append(var)
		indice = indice + 1
		types.append(prob.variables.type.binary)


	alpha = 0.001
	debut_indice_flow = indice
	for i in tab_sommets[1:]:
		for j in tab_sommets[1:]:
			if j != i:
				obj.append(alpha)
				var = "f_" + str(i) + "_" + str(j)
				str_ind[var] = indice
				ind_str[indice] = var
				my_colnames.append(var)
				indice = indice + 1
				types.append(prob.variables.type.integer)
				#types.append(prob.variables.type.continuous)



	#lower bound est par défault à 0.0 donc on ne spécifie pas.
	#Il faut spécifier upper bounds ?

	prob.variables.add(obj = obj, types = types, names = my_colnames)
	print("Fait")
	#On va construire les contraintes:
	rows = []
	my_rhs = []
	my_sense = []
	my_rownames = []

	print("1")
	
	#Contrainte 1:
	my_rhs.append(float(n - 1))
	my_sense.append('E')
	my_rownames.append("C1")
	i = racine
	tab1 = []
	tab2 = []
	for j in tab_sommets[2:]:
		tab1.append(str_ind.get("f_" + str(i) + "_" + str(j)))
		tab2.append(str_ind.get("f_" + str(j) + "_" + str(i)))
	rows.append([tab1 + tab2,[1]*(len(tab1)) + [-1]*(len(tab2))])

	prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
								rhs=my_rhs, names=my_rownames)

	rows = []
	my_rhs = []
	my_sense = []
	my_rownames = []
	
	print("2")
	#Contraintes 2:
	compteur = 0
	for i in tab_sommets[2:]:
		compteur = compteur + 1
		my_rhs.append(float(-1))
		my_sense.append('E')
		my_rownames.append("C2_" + str(compteur))
		tab1 = []
		tab2 = []
		for j in tab_sommets[1:]:
			if j != i:
				tab1.append(str_ind.get("f_" + str(i) + "_" + str(j)))
				tab2.append(str_ind.get("f_" + str(j) + "_" + str(i)))
		rows.append([tab1 + tab2, [1]*(len(tab1)) + [-1]*(len(tab2))])
		prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
								rhs=my_rhs, names=my_rownames)
		rows = []
		my_rhs = []
		my_sense = []
		my_rownames = []

	
	
	print("3")
	#Contraintes 3:
	compteur = 0
	for i in tab_sommets[2:]:
		for j in tab_sommets[2:]:
			if j > i:
				compteur = compteur + 1
				my_rhs.append(float(0))
				my_sense.append('L')
				my_rownames.append("C3_" + str(compteur))
				rows.append([[str_ind.get("f_" + str(i) + "_" + str(j)), str_ind.get("f_" + str(j) + "_" + str(i)),
				str_ind.get("x1_" + str(i) + "_" + str(j)), str_ind.get("x2_" + str(i) + "_" + str(j))], [1,1,-1,-(n-2)]])

	prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
								rhs=my_rhs, names=my_rownames)
	
	rows = []
	my_rhs = []
	my_sense = []
	my_rownames = []
	
	print("4")
	#Contraintes 4:
	compteur = 0
	for j in tab_sommets[2:]:
		i = racine
		if j < i:
			(i,j) = (j,i)
		compteur = compteur + 1
		my_rhs.append(float(0))
		my_sense.append('L')
		my_rownames.append("C4_" + str(compteur))
		rows.append([[str_ind.get("f_" + str(i) + "_" + str(j)), str_ind.get("f_" + str(j) + "_" + str(i)),
		str_ind.get("x1_" + str(i) + "_" + str(j)), str_ind.get("x2_" + str(i) + "_" + str(j)), str_ind.get("x3_" + str(i) + "_" + str(j))],
		[1,1,-1, -(n-2), -(n-1)]])

	prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
								rhs=my_rhs, names=my_rownames)
	
	rows = []
	my_rhs = []
	my_sense = []
	my_rownames = []


	print("5")
	#Contraintes 5:
	compteur = 0
	for j in tab_sommets[2:]:
		i = racine
		if j < i:
			(i,j) = (j,i)
		compteur = compteur + 1
		my_rhs.append(float(0))
		my_sense.append('L')
		my_rownames.append("C5_" + str(compteur))
		rows.append([[str_ind.get("x3_" + str(i) + "_" + str(j)), str_ind.get("f_" + str(i) + "_" + str(j)),
		str_ind.get("f_" + str(j) + "_" + str(i))], [(n-1),-1,-1]])

	prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
								rhs=my_rhs, names=my_rownames)
	
	rows = []
	my_rhs = []
	my_sense = []
	my_rownames = []

	
	print("6")
	#Contrainte 6:
	tab1 = []
	for i in tab_sommets[1:]:
		for j in tab_sommets[1:]:
			if j > i:
				fin = 3
				if i == racine or j == racine:
					fin = 4
				for k in range(1,fin):
					tab1.append(str_ind.get("x" + str(k) + "_" + str(i) + "_" + str(j)))

	my_rhs.append(float(n-1))
	my_sense.append('E')
	my_rownames.append("C6")
	rows.append([tab1,[1]*(len(tab1))])

	prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
								rhs=my_rhs, names=my_rownames)
	
	rows = []
	my_rhs = []
	my_sense = []
	my_rownames = []

	print("7")
	#Contrainte 7:
	tab1 = []
	for j in tab_sommets[2:]:
		i = racine
		if j < i:
			(i,j) = (j,i)
		tab1.append(str_ind.get("x3" + "_" + str(i) + "_" + str(j)))

	my_rhs.append(float(1))
	my_sense.append('L')
	my_rownames.append("C7")
	rows.append([tab1,[1]*(len(tab1))])

	prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
								rhs=my_rhs, names=my_rownames)
	
	rows = []
	my_rhs = []
	my_sense = []
	my_rownames = []

	print("8")
	#Contraintes 8:
	compteur = 0
	for i in tab_sommets[1:]:
		for j in tab_sommets[1:]:
			if j > i:
				compteur = compteur + 1
				tab1 = []
				fin = 3
				if i == racine or j == racine:
					fin = 4
				for k in range(1,fin):
					tab1.append(str_ind.get("x" + str(k) + "_" + str(i) + "_" + str(j)))
				my_rhs.append(float(1))
				my_sense.append('L')
				my_rownames.append("C8_" + str(compteur))
				rows.append([tab1,[1]*(len(tab1))])

	print("Fait")		



	prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
								rhs=my_rhs, names=my_rownames)

	return debut_indice_flow






def resolution_cplex(nb_sommet, tab_sommets, tab_cout1, tab_cout2):

	prob = cplex.Cplex()

	#On indique c'est un problème linéaire en nombre entier.
	prob.set_problem_type(cplex.Cplex.problem_type.MILP)
	#On veut minimiser
	prob.objective.set_sense(prob.objective.sense.minimize)
	#prob.parameters.mip.tolerances.integrality = 0.0
	#prob.parameters.mip.limits.solutions = 5
	#prob.parameters.simplex.limits.iterations = 15
	#prob.parameters.mip.strategy.probe = 3
	#prob.parameters.timelimit = 25
	#prob.parameters.simplex.limits.iterations = 15


	
	print("Ecriture problème")
	debut_indice_flow = populatebyrow(prob, tab_sommets, tab_cout1, tab_cout2)
	print("fait")
	#prob.parameters.tune_problem()
	#prob.parameters.mip.tolerances.mipgap = 0.7
	#prob.parameters.mip.tolerances.absmipgap = 1000
	#prob.parameters.mip.limits.nodes = 50
	#prob.parameters.barrier.limits.iteration = 10
	prob.solve()

	numrows = prob.linear_constraints.get_num()
	numcols = prob.variables.get_num()

	print()
	# solution.get_status() returns an integer code
	print("Solution status = ", prob.solution.get_status(), ":", end=' ')
	# the following line prints the corresponding string
	print(prob.solution.status[prob.solution.get_status()])
	print("Solution value  = ", prob.solution.get_objective_value())
	slack = prob.solution.get_linear_slacks()
	#pi = prob.solution.get_dual_values()
	x = prob.solution.get_values()
	#print(prob.variables.get_names()[debut_indice_flow:])
	#dj = prob.solution.get_reduced_costs()

	#La solution réside dans les flots différents de 0
	names_flow = prob.variables.get_names()[debut_indice_flow:]

	#Il nous faut une correspondance entre le numéro des sommets et les indices du tableau
	dict_sommet_indice = {}
	for i in range(1,nb_sommet + 1):
		dict_sommet_indice[tab_sommets[i]] = i

	tree = [0]*(nb_sommet + 1)
	tree[1] = 1
	for i, item in enumerate(x[debut_indice_flow:]):
		if round(item) != 0:
			tab = names_flow[i].split("_")
			sommet1 = dict_sommet_indice.get(int(tab[1]))
			sommet2 = dict_sommet_indice.get(int(tab[2]))
			tree[sommet2] = sommet1

	return TreeStruct(nb_sommet, -1, 1, tree, tab_cout1, tab_cout2, tab_sommets)





if __name__ == "__main__":
	resolution_cplex()