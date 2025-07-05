import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.numCompagnie = None
        self.valore_ddArr = None
        self.valore_ddDep = None

    def read_casellaTesto_intero(self):
        numCompagnie = self._view.tf_compagnie.value
        try:
            numCompagnie = int(numCompagnie)
            self.numCompagnie = numCompagnie
            print(f"numCompagnie: {self.numCompagnie} {type(numCompagnie)}")
            return True
        except ValueError:
            self._view.create_alert("inserire valore valido")
            return False

    def handle_creaGrafo(self, e):
        self._view.lv_result.controls.clear()
        self._view.update_page()
        self._view.show_loading_bar()
        self.read_casellaTesto_intero()
        if self.numCompagnie is None:
            self._view.create_alert("inserire numero compagnie")
            return
        self._model.build_graph(self.numCompagnie)
        self._view.lv_result.controls.append(ft.Text(self._model.grafo))
        self.fill_dropdown()
        self._view.remove_loading_bar()
        self._view.update_page()

    def handle_verificaConnessione(self, e):
        self._view.lv_result.controls.clear()
        self._view.update_page()
        G = self._model.grafo
        connessi = nx.node_connected_component(G, self.valore_ddDep)  # restituisce Un set contenente tutti i nodi
                                                # che fanno parte della componente connessa
                                                # a cui appartiene il nodo specificato
        for n in connessi:
            if n==self.valore_ddArr:
                self._view.lv_result.controls.append(ft.Text(f"{self.valore_ddDep} e {self.valore_ddArr} sono connessi"))
                path = self._model.get_path(self.valore_ddDep, self.valore_ddArr)
                self._view.lv_result.controls.append(ft.Text(f"shortest path secondo algoritmo di dijkstra per attributo weight: "))
                for ar in path:
                    self._view.lv_result.controls.append(ft.Text(ar))
                self._view.lv_result.controls.append(ft.Text(f"componenti shortest path {len(path)}"))
                self._view.update_page()
                return
        self._view.lv_result.controls.append(ft.Text(f"nessuna connessione"))

        self._view.update_page()


    def fill_dropdown(self):
        if self._model.grafo.nodes is None:
            self._view.create_alert("crea un grafo!")
            return
        lista_opzioni = list(self._model.grafo.nodes)
        for o in lista_opzioni:
            self._view.dropdown1.options.append(ft.dropdown.Option(key=o,
                                                                  text=o,
                                                                  data=o,
                                                                  on_click=self.read_dropdownDep))
            self._view.dropdown2.options.append(ft.dropdown.Option(key=o,
                                                                   text=o,
                                                                   data=o,
                                                                   on_click=self.read_dropdownArr))

    def read_dropdownDep(self, e):
        self.valore_ddDep = e.control.data
        print(f"valore letto partenza: {self.valore_ddDep} - {type(self.valore_ddDep)}")

    def read_dropdownArr(self, e):
        self.valore_ddArr = e.control.data
        print(f"valore letto destinazione: {self.valore_ddArr} - {type(self.valore_ddArr)}")

