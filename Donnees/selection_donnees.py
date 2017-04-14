#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import numpy as np
import random
import pickle

def select_sample(nb_sommet_total,nb_sample):
	
	all_sommet = list(range(1,nb_sommet_total + 1))
	# Obtenir échantillon de 6 éléments  
	tab_sommets = random.sample(all_sommet, nb_sample)
	return tab_sommets