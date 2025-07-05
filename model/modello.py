import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.idMapAirports = DAO.getAllAirports()

    def build_graph(self, numCompagnie):
        self.grafo = None
        self.grafo = nx.Graph()
        for nodeID in self.get_nodes_prog(numCompagnie):
            self.grafo.add_node(self.idMapAirports[nodeID])

        for n1 in list(self.grafo.nodes):
            for n2 in list(self.grafo.nodes):
                w = DAO.get_edge_weight(n1.ID, n2.ID)
                if w > 0 and (n1, n2) not in list(self.grafo.edges) and (n2, n1) not in list(self.grafo.edges):
                    self.grafo.add_edge(n1, n2, weight=w)

    def get_nodes_prog(self, numCompagnie):
        nodesID = set()
        for key in self.idMapAirports.keys():
            setAirlinesArr = DAO.get_arr_airlines(key)
            setAirlinesDep = DAO.get_dep_airlines(key)
            distinctAirlines = setAirlinesArr|setAirlinesDep
            #print(f"airportID: {key} -- airlines: {distinctAirlines} -- tot: {len(distinctAirlines)}")
            if len(distinctAirlines) >= numCompagnie:
                nodesID.add(key)
        return nodesID

    def get_path(self, source, target):
        sp = nx.dijkstra_path(self.grafo, source, target, weight='weight')
        return sp



if __name__ == '__main__':
    m = Model()
    m.build_graph(12)
    print(m.grafo)
    for e in m.grafo.edges():
        peso = m.grafo[e[0]][e[1]]['weight']
        print(e, f"peso: {peso}")
