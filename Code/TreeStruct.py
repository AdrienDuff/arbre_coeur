import numpy as np

class TreeStruct(object):
	"""docstring for TreeStruct:
	- nSommet nombre de sommets
	- generation sa génération
	- numero le numéro de l'arbre
	- tree le tableau de structure"""

	def __init__(self):
		self.nSommet = 7
		self.generation = 1
		self.numero = 1
		self.tree = [0,1,1,4,1,4,4,6]

	def cout(self):
		for i in range(2,self.nSommet+1):
			print("arc :" + str(i) + str(self.tree[i]) )

