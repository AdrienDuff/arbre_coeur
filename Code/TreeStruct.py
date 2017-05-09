import numpy as np
import sys
from calcul_cout import *
import networkx as nx
import plotly
import plotly.plotly as py
from plotly.graph_objs import *


class TreeStruct(object):
	"""docstring for TreeStruct:
	- nSommet nombre de sommets de l'arbre
	- generation  : numéro de sa génération
	- numero : le numéro de l'arbre dans sa génération
	- tree : le tableau de parents : On y stocke les indices de tab_sommets"""

	def __init__(self,n_s,n_gene,n_num, tree,tab_cout1, tab_cout2, tab_sommets):
		self.nSommet = n_s
		self.generation = n_gene
		self.numero = n_num
		self.tree = tree
		self.tab_cout1 = tab_cout1
		self.tab_cout2 = tab_cout2
		self.cout = -1
		self.racine_feuille = -1
		self.tab_sommets = tab_sommets


	def calcul_cout(self):
		"""
		for i in range(2, self.nSommet + 1):
			Node1 = i
			Node2 = self.tree[i]
			print(Node2, " ", Node1, "c1 :", getcout(self.tab_cout1,self.tab_sommets[Node1],self.tab_sommets[Node2]), " c2:", getcout(self.tab_cout2,self.tab_sommets[Node1],self.tab_sommets[Node2]))
		"""
		c = 0
		self.racine_feuille = True
		nb_racine = 0
		indice = 2
		#On vérifie si 1 est racine ou pas.
		while indice <= self.nSommet and self.racine_feuille == True:
			if self.tree[indice] == 1:
				nb_racine += 1
			if nb_racine >= 2:
				self.racine_feuille = False
			indice += 1
		#print(self.racine_feuille)

		for i in range(2,self.nSommet+1):
			#Le 1 est un cas pathologique à traiter à part car c'est la racine de l'arbre
			if self.tree[i] == 1 and self.racine_feuille:
				c += getcout(self.tab_cout1,self.tab_sommets[1],self.tab_sommets[i])
			else:
				#Le cout que l'on prend dépend si i apparait ou non dans la liste.
				#Si on est dans le réseau, on prend le cout 2, sinon le cout 1
				if i in self.tree:
					c += getcout(self.tab_cout2,self.tab_sommets[self.tree[i]],self.tab_sommets[i])
				else:
					c += getcout(self.tab_cout1,self.tab_sommets[self.tree[i]],self.tab_sommets[i])
		self.cout = c
		return c



	def dessine_toi(self, tab_sommets, tab_coord):
		G=nx.Graph()
		#On ajoute les sommets
		for sommet in range(1,self.nSommet + 1):
			G.add_node(sommet, pos=(tab_coord[tab_sommets[sommet]][1],tab_coord[tab_sommets[sommet]][2]))

		#On ajoute les arcs
		for edge in range(1,self.nSommet + 1):
			#Si on a pas la racine
			if edge != self.tree[edge]:
				G.add_edge(edge,self.tree[edge])


		edge_trace = Scatter(
		    x=[],
		    y=[],
		    line=Line(width=1,color='#888'),
		    hoverinfo='none',
		    mode='lines')

		for edge in G.edges():
		    x0, y0 = G.node[edge[0]]['pos']
		    x1, y1 = G.node[edge[1]]['pos']
		    edge_trace['x'] += [x0, x1, None]
		    edge_trace['y'] += [y0, y1, None]

		node_trace = Scatter(
		    x=[],
		    y=[],
		    text=[],
		    mode='markers',
		    hoverinfo='text',
		    marker=Marker(
		        showscale=True,
		        # colorscale options
		        # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
		        # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
		        colorscale='Bluered',
		        reversescale=False,
		        color=[],
		        size=4,
		        colorbar=dict(
		            thickness=1,
		            title='Node Connections',
		            xanchor='left',
		            titleside='right'
		        ),
		        line=dict(width=1)))

		for node in G.nodes():
			x, y = G.node[node]['pos']
			node_trace['x'].append(x)
			node_trace['y'].append(y)
			node_info = 'node :' + str(node)
			node_trace['text'].append(node_info)

		for node, adjacencies in enumerate(G.adjacency_list()):
			if len(adjacencies) == 1:
				node_trace['marker']['color'].append(1)
			else:
				node_trace['marker']['color'].append(2)
			node_info =' # of connections: '+str(len(adjacencies))
			node_trace['text'].append(node_info)


		fig = Figure(data=Data([edge_trace, node_trace]),
		             layout=Layout(
		                title='<br>Génération ' + str(self.generation) + ', Numéro: ' + str(self.numero) + ', Cout :' + str(self.cout),
		                titlefont=dict(size=16),
		                showlegend=False,
		                #scene = Scene(aspectmode = "cube"),
		                #autosize=False,
    					#width=700,
    					#height=700,
		                hovermode='closest',
		                margin=dict(b=20,l=5,r=5,t=40),
		                annotations=[ dict(
		                    text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
		                    showarrow=False,
		                    xref="paper", yref="paper",
		                    x=0.005, y=-0.002 ) ],
		                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
		                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

		#py.iplot(fig, filename='networkx')
		plotly.offline.plot(fig, filename='networkx_' + str(self.generation) + "_" + str(self.numero) + '.html')



