import copy
from itertools import combinations

import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.load_all_artists()
        self.artist_map={}
        self.nodi=[]
        self.G=nx.Graph()

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()

        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):

        for a in self._artists_list:
            self.artist_map[a.id] = a

        self.artist_id_album=DAO.get_artists_album(min_albums)


    def build_graph(self):
        for id in self.artist_id_album:
            self.nodi.append(self.artist_map[id])

        self.G.add_nodes_from(self.nodi)
        self.diz_archi={}
        self.connessioni=DAO.get_generi()
        print(self.connessioni)

        for c1 in self.connessioni:
            if c1.genere not in self.diz_archi:
                self.diz_archi[c1.genere] =set()
                self.diz_archi[c1.genere].append(c1.artist)
            else :
                self.diz_archi[c1.genere].append(c1.artist)

        for g in self.diz_archi:

            lista_archi=list(combinations(self.diz_archi[g], 2))

            self.G.add_edges_from(lista_archi)
        print(self.G)

    def get_artist_map(self):
        return self.artist_map
    def get_artisti(self):
        return self._artists_list

    def get_vicini(self,artista):
        vicini=list(self.G.neighbors(artista))
        vicini_ordinati=sorted(vicini, key=lambda x: vicini.id)
        return vicini_ordinati

    def get_cammino(self,n_art,artista,n_min):
        self.best_bercorso=[]
        self.best_peso=0

        partial=[artista]
        self.ricorsione(partial,0,n_art,n_min)
        return self.best_bercorso

    def ricorsione(self,partial,peso,n_art,n_min):
        if len(partial)==n_art:
            if peso>self.best_peso:
                self.best_bercorso=copy.deepcopy(partial)
                self.best_peso=peso
            return

        n_last=partial[-1]
        for v in self.G.neighbors(n_last):
            if v.durata/60000 < n_min:
                partial.append(v)
                peso_arco=self.G.get_edge_data(n_last,v)['weight']
                if peso_arco+peso<self.best_peso:
                    self.ricorsione(partial,peso_arco+peso,n_art,n_min)
                    partial.pop()

#prova