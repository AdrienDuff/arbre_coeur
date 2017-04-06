from tulip import *
import tulipplugins

class main(tlp.BooleanAlgorithm):
  def __init__(self, context):
    tlp.BooleanAlgorithm.__init__(self, context)
    # You can add parameters to the plugin here through the following syntax:
    # self.add<Type>Parameter("<paramName>", "<paramDoc>", "<paramDefaultValue>")
    # (see the documentation of class tlp.WithParameter to see what parameter types are supported).

  def check(self):
    # This method is called before applying the algorithm on the input graph.
    # You can perform some precondition checks here.
    # See comments in the run method to know how to have access to the input graph.

    # Must return a tuple (Boolean, string). First member indicates if the algorithm can be applied
    # and the second one can be used to provide an error message.
    return (True, "")
 
  
  
  def run(self):
    #Une implementation de union-find
    tlp.node.parent = ""
    tlp.node.rank = ""
    print hasattr(tlp.node(), 'parent')
    dict_parent = {}
    def MakeSet(x):
     
      x.parent = x
      x.rank   = 0
      
    def Union(x, y):
      xRoot = Find(x)
      yRoot = Find(y)
      if xRoot.rank > yRoot.rank:
          yRoot.parent = xRoot
      elif xRoot.rank < yRoot.rank:
          xRoot.parent = yRoot
      elif xRoot != yRoot: # Unless x and y are already in same set, merge them
          yRoot.parent = xRoot
          xRoot.rank = xRoot.rank + 1
    
    def Find(x):
      if x.parent == x:
         return x
      else:
         x.parent = Find(x.parent)
         return x.parent

    viewSelection = self.graph.getBooleanProperty("viewSelection")
    viewMetric = self.graph.getDoubleProperty("viewMetric")
    n = self.graph.numberOfNodes()
    edge_tab = []
    #On cree un nouveau graphe
    new_graph = self.graph.addSubGraph("arbre_couvrant")
    for node in self.graph.getNodes():
      MakeSet(node)
      print node
      print node.parent
      print id(node)
      new_graph.addNode(node)
    
    for edge in self.graph.getEdges():
      edge_tab.append(edge)
      print self.graph.source(edge)
      print id(self.graph.source(edge))
      print self.graph.source(edge).parent
      
    def getweight(edge):
      return  viewMetric[edge]
      
    edge_tab.sort(key = getweight)
    #Nous avons un tableau d'arretes trie.
    #On commence l'algo. On s'arrete si on a pris (n-1) arretes ou si on ne trouve pas d'arrete. n est le nombre de sommet.
    compteur = 1
    edge_found = True
    indice = 0
    while compteur < n and edge_found:
      #On cherche la premiere arrete qui ne cree pas de cycles
      edge_found = False
      while not edge_found:
        edge_to_test = edge_tab[indice]   
        if Find(self.graph.source(edge_to_test)) != Find(self.graph.target(edge_to_test)):
          edge_found = True
          new_graph.addEdge(edge_to_test)
          Union(self.graph.source(edge_to_test),self.graph.target(edge_to_test))
        indice += 1
     
      
      compteur += 1

    params = tlp.getDefaultPluginParameters('Acyclic', self.graph)

    success = self.graph.applyAlgorithm('Acyclic', params)
    print success

    return True

# The line below does the magic to register the plugin into the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPlugin("main", "coeur_kruskal", "Adrien et benjamin", "06/03/2017", "", "0.1")
