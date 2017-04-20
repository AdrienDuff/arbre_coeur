import numpy as np
import sys
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

	def __init__(self,n_s,n_gene,n_num, tree):
		self.nSommet = n_s
		self.generation = n_gene
		self.numero = n_num
		self.tree = tree


	def cout(self):
		for i in range(2,self.nSommet+1):
			print("arc :" + str(i) + str(self.tree[i]))

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
		    line=Line(width=0.5,color='#888'),
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
		        colorscale='YIGnBu',
		        reversescale=True,
		        color=[],
		        size=1,
		        colorbar=dict(
		            thickness=15,
		            title='Node Connections',
		            xanchor='left',
		            titleside='right'
		        ),
		        line=dict(width=2)))

		for node in G.nodes():
		    x, y = G.node[node]['pos']
		    node_trace['x'].append(x)
		    node_trace['y'].append(y)

		for node, adjacencies in enumerate(G.adjacency_list()):
		    node_trace['marker']['color'].append(len(adjacencies))
		    node_info = '# of connections: '+str(len(adjacencies))
		    node_trace['text'].append(node_info)


		fig = Figure(data=Data([edge_trace, node_trace]),
		             layout=Layout(
		                title='<br>Network graph made with Python',
		                titlefont=dict(size=16),
		                showlegend=False,
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
		plotly.offline.plot(fig, filename='networkx' + str(self.numero) + '.html')



