"""
----------------Costruzione Grafi e NetworkX-----------------

NetworkX viene utilizzato dal Model per rappresentare le relazioni tra i dati estratti dal DAO attraverso i grafi

Tipologie di grafi: > G. NON ORIENTATO: Le connessioni sono BIDIREZIONALI -> Se esiste l'arco A-B allora esiste anche B-A

                                       Classe nx: nx.Graph()

                    > G. ORIENTATO: Le connessioni hanno un VERSO -> L'arco A-B NON equivale all'arco B-A

                                    Classe nx: nx.DiGraph()

                    > G. PESATO: In aggiunta ai precedenti, ogni arco ha un valore numerico associato (PESO)

                    > G. SEMPLICE: Massimo un arco tra due nodi e nessun self-loop

                    > MULTIGRAFO: Permette più archi tra gli stessi due nodi

                                  Classe nx: nx.MultiGraph()

!!! La libreria da importare è: import networkx as nx
"""

#----------------Creazione e Struttura del Grafo--------------

G = nx.Graph()                      #Creazione grafo NON orientato

G = nx.DiGraph()                    #Creazione grafo ORIENTATO

G.clear()                           #Pulisce il grafo (Fondamentale per ricalcolare i dati con nuovi filtri)

G.add_node(obj)                     #Aggiunge un nodo al grafo (obj può essere un ID o un intero OGGETTO del Model (!!! Dotato di metodo __hash__))
G.add_nodes_from(lista_nodi)        #Aggiunge nodi dalla lista passata come parametro

G.add_edge(u, v, weight=w)          #Crea un arco tra u e v con peso w
G.add_edges_from(lista_archi)       #Crea gli archi all'interno della lista


#-----------------Esplorazione e Proprietà del Grafo-------------

G.number_of_nodes()                 #Restituisce il numero totale di nodi inseriti
G.number_of_edges()                 #Restituisce il numero totale di archi creati

G.edges(data=True)                  #otteniamo una tripla di dati del tipo tratta = (u, v, attributi)

G.degree(n)                         #Restituisce il numero di archi incidenti sul nodo n
G.degree(n, weight='weight')        #Restituisce la somma totale dei pesi degli archi collegati al nodo

list(G.neighbors(n))                #Restituisce la lista di nodi ADIACENTI a n (Fonfamentale per la ricorsione)

nx.node_connected_component(G, nodo_sorgente)     #Restituisce un set contenente tutti i nodi che appartengono alla stessa componente connessa del nodo di partenza (Raggiungibili)


#----------------------Gestione Pesi archi-----------------------

for u, v, data in G.edges(data=True):
    peso = data['weight']

    if peso < / > soglia / valore:        #Condizione sul peso
        #azione




#Esempio Lab10 (Hub e tratte spedizioni)
class Model:
    def __init__(self):
                # self._nodes = None
                # self._edges = None
                self.G = nx.Graph()
                self._lista_hub = []  # Nodes
                self._lista_tratte = []  # Edges
                self._dizionario_hub = {}

    def costruisci_grafo(self, threshold):
        self.G.clear()  # Pulisco il grafo in modo da non sovrascriverlo ogni volta
        self._lista_hub = DAO.get_hub()  # Lista di oggetti Hub
        self._lista_tratte = DAO.get_tratta()  # Lista di oggetti Tratta

        for hub in self._lista_hub:  # Ciclo sui nodi
            self.G.add_node(hub)  # Aggiungo ogni hub alla lista dei nodi
            self._dizionario_hub[hub.id] = hub  # Creo il dizionario di hub per poter aggiungere più facilmente le tratte

            # OPPURE: self.G.add_nodes_from(self._lista_hub)

        for tratta in self._lista_tratte:  # Ciclo sulle tratte
            if tratta.guadagno_medio >= threshold:  # Condizione sul guadagno minimo
                self.G.add_edge(self._dizionario_hub[tratta.id_hub_A], self._dizionario_hub[tratta.id_hub_B], weight=tratta.guadagno_medio)

        return self.G

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_tratte(self, e):
        self._view.lista_visualizzazione.controls.clear()        #Pulisco la lista
        self._view.page.update()                                 #Aggiorno la pagina

        threshold_str = self._view.guadagno_medio_minimo.value

        try:                                 #Verifica che il valore inserito non sia una stringa
            if  not threshold_str:
                threshold = 0.0
            else:
                threshold = float(threshold_str)

        except ValueError:
            self._view.show_alert("Inserire un valore numerico valido")
            self._view.page.update()
            return


        grafo = self._model.costruisci_grafo(threshold)      #Costruisco il grafo con l'apposita funzione

        self._view.lista_visualizzazione.controls.append(ft.Row(controls=[ft.Text("Numero di tratte: "), ft.Text(str(self._model.get_num_edges()))]))
        self._view.lista_visualizzazione.controls.append(ft.Row(controls=[ft.Text("Numero di nodi: "), ft.Text(str(self._model.get_num_nodes()))]))

        tratte = grafo.edges(data=True)        #Con la funzione grafo.edges(data=True) otteniamo una tripla di dati del tipo tratta = (u, v, attributi)

        for u, v, data in tratte:              #Cilciamo su ogni tripla ottenuta (ognuna rappresentante una tratta)
            guadagno = data.get('weight', 'N/D')
            self._view.lista_visualizzazione.controls.append(ft.Text(f"Hub {u} --> Hub {v} - Valore tratta : {guadagno}"))

        #u e v sono di tipo Hub dato che abbiamo inizializzato tutti i nodi come oggetti Hub
        #-> Quando andremo a stampare u e v verrà utilizzata la funzione __str__ degli oggetti Hub

        self._view.page.update()          #Aggiorno la pagina


#Esempio Lab11 (Rifugi e sentieri)

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._lista_rifugi = []   #Nodes
        self._dizionario_rifugi = {}
        self._lista_connessioni = []    #Connessioni

    def build_graph(self, year: int):
        self.G.clear()               #Puliamo il grafo per evitare di sovrascrivere il grafo precedente

        #Crea lista rifugi -> nodes
        self._lista_rifugi = DAO.get_rifugio()
        #Aggiunta nodes al dizionario dei rifugi
        for rifugio in self._lista_rifugi:
            self._dizionario_rifugi[rifugio.id] = rifugio


        #Crea lista connessioni -> edges
        self._lista_connessioni = DAO.get_connessione_per_anno(year)
        #Aggiunta edges al grafo
        for connessione in self._lista_connessioni:
            self.G.add_edge(self._dizionario_rifugi[connessione.id_1], self._dizionario_rifugi[connessione.id_2],  weight=connessione.anno)

        return self.G


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self._current_rifugio = None

    def handle_calcola(self, e):
        year = self._view.txt_anno.value
        try:
            year_n = int(year)
        except (ValueError, TypeError):
            self._view.show_alert("Inserisci un valore numerico nel campo anno.")
            return

        if year_n < 1950 or year_n > 2024:
            self._view.show_alert("Inserisci un valore compreso tra 1950 e 2024.")
            return

        # costruisce il grafo con il model
        self._model.build_graph(year_n)

        # aggiorna l'area risultati
        self._view.lista_visualizzazione.controls.clear()
        # uso il metodo corretto per il numero di componenti
        num_cc = self._model.get_num_connected_components()
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Il grafo ha {num_cc} componenti connesse."))
        self._view.lista_visualizzazione.controls.append(ft.Text("Di seguito il dettaglio sui nodi:"))

        for n in self._model.get_nodes():
            # n è un oggetto rifugio; usiamo .nome come rappresentazione
            grado = self._model.get_num_neighbors(n)
            self._view.lista_visualizzazione.controls.append(ft.Text(f"{n} -- {grado} vicini."))

        # abilita dropdown e bottone raggiungibili (se erano disabilitati)
        self._view.dd_rifugio.disabled = False
        self._view.pulsante_raggiungibili.disabled = False

        # riempie il dropdown con i rifugi attuali
        self._fill_dropdown()
        self._view.update()


#Esempio Lab12 (Rifugi e sentieri)

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self._lista_rifugi = []
        self._dizionario_rifugi = {}
        self._lista_connessioni = []

        self._lista_pesi = []


    def build_weighted_graph(self, year: int):
        self.G.clear()                  #Puliamo il grafo per non sovrascrivere
        self._lista_rifugi.clear()
        self._lista_connessioni.clear()
        self._lista_rifugi = DAO.get_rifugio()
        self._lista_connessioni = DAO.get_connessioni_per_anno(year)

        for rifugio in self._lista_rifugi:
            self._dizionario_rifugi[rifugio.id] = rifugio

        for connessione in self._lista_connessioni:
            peso = (float(connessione.distanza) * float(connessione.converti_difficolta(connessione.difficolta)))
            self.G.add_edge(self._dizionario_rifugi[connessione.id_1], self._dizionario_rifugi[connessione.id_2],  weight = peso )
            self._lista_pesi.append(peso)

        return self.G

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_grafo(self, e):
        try:
            anno = int(self._view.txt_anno.value)
        except:
            self._view.show_alert("Inserisci un numero valido per l'anno.")
            return
        if anno < 1950 or anno > 2024:
            self._view.show_alert("Anno fuori intervallo (1950-2024).")
            return

        self._model.build_weighted_graph(anno)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo calcolato: {self._model.G.number_of_nodes()} nodi, {self._model.G.number_of_edges()} archi")
        )
        min_p, max_p = self._model.get_edges_weight_min_max()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Peso min: {min_p:.2f}, Peso max: {max_p:.2f}"))
        self._view.page.update()


#Esempio Week10 (Metro Paris)

class Model:
    def __init__(self):
        self._lista_fermate = []
        self._dizionario_fermate = {}
        self._grafo = None

    def getAllFermate(self):
        fermate = DAO.readAllFermate()
        self._lista_fermate = fermate
        # Mi sono costruito un dizionario di fermate, con chiave
        # l'id_fermata e valore l'oggetto fermata corrispondente
        for fermata in self._lista_fermate:
            self._dizionario_fermate[fermata.id_fermata] = fermata


    def creaGrafo(self):
        self._grafo = nx.MultiDiGraph() # Posso avere più archi tra due nodi
        for fermata in self._lista_fermate:
            self._grafo.add_node(fermata)
        # PRIMO MODO DI AGGIUNGERE GLI ARCHI, CON 619*619 QUERY SQL
        """
        for u in self._grafo: # Per ognuno dei 619 nodi
            for v in self._grafo: # Per ognuno dei possbili nodi connessi
                risultato = DAO.existsConnessioneTra(u, v)
                if(len(risultato) > 0): # C'è almeno una connessione
                    self._grafo.add_edge(u, v) # Creo l'arco
                    print(f"Aggiunto arco tra {u} e {v}")
        """

        # SECONDO MODO, CON 619 QUERY A CERCARE I NODI VICINI
        """
        conta = 0
        for u in self._grafo:
            connessioniAVicini = DAO.searchViciniAFermata(u)
            for connessione in connessioniAVicini:
                fermataArrivo = self._dizionario_fermate[connessione.id_stazA]
                self._grafo.add_edge(u, fermataArrivo)
                print(f"Aggiunto arco tra {u} e {fermataArrivo}")
                print(len(self._grafo.edges()))
        """

        # TERZO MODO, CON UNA QUERY SOLA CHE ESTRAE IN UN COLPO SOLO TUTTE LE CONN.
        """
        listaConnessioni = DAO.readAllConnessioni()
        for c in listaConnessioni:
            u_nodo = self._dizionario_fermate[c.id_stazP]
            v_nodo = self._dizionario_fermate[c.id_stazA]
            self._grafo.add_edge(u_nodo, v_nodo)
            print(f"Aggiunto arco tra {u_nodo} e {v_nodo}")
        """

        # COSTRUISCO UN GRAFO PESATO
        """
        listaConnessioni = DAO.readAllConnessioni()
        for c in listaConnessioni:
            u_nodo = self._dizionario_fermate[c.id_stazP]
            v_nodo = self._dizionario_fermate[c.id_stazA]
            #print(f"{self._grafo[u_nodo][v_nodo]}")
            if self._grafo.has_edge(u_nodo, v_nodo):
                self._grafo[u_nodo][v_nodo]["peso"] += 1
            else:
                self._grafo.add_edge(u_nodo, v_nodo, peso=1)

            print(f"Aggiunto arco tra {u_nodo} e {v_nodo}, peso: {self._grafo[u_nodo][v_nodo]}")
        """
        # COSTRUISCO UN MULTI-GRAFO NEL QUALE IL PESO DEGLI ARCHI E' IL T. PERCORR.
        listaConnessioni = DAO.readAllConnessioni()
        for c in listaConnessioni:
            u_nodo = self._dizionario_fermate[c.id_stazP]
            v_nodo = self._dizionario_fermate[c.id_stazA]
            punto_u = (u_nodo.coordX, u_nodo.coordY)
            punto_v = (v_nodo.coordX, v_nodo.coordY)
            distanza = geodesic(punto_u, punto_v).km
            velocita = DAO.readVelocita(c._id_linea)
            print(f"Distanza: {distanza}, velocità: {velocita}")
            tempo_perc = distanza / velocita * 60 # Tempo percorrenza in min.
            self._grafo.add_edge(u_nodo, v_nodo, tempo = tempo_perc)
            print(f"Aggiunto arco tra {u_nodo} e {v_nodo}, tempo: {self._grafo[u_nodo][v_nodo]}")

        # COSTRUISCO UN GRAFO (NON MULTI) NEL QUALE IL PESO DEGLI ARCHI E' IL T. PERCORR.
        listaConnessioni = DAO.readAllConnessioni()
        for c in listaConnessioni:
            u_nodo = self._dizionario_fermate[c.id_stazP]
            v_nodo = self._dizionario_fermate[c.id_stazA]
            punto_u = (u_nodo.coordX, u_nodo.coordY)
            punto_v = (v_nodo.coordX, v_nodo.coordY)
            distanza = geodesic(punto_u, punto_v).km
            velocita = DAO.readVelocita(c._id_linea)
            tempo_perc = distanza / velocita * 60  # Tempo percorrenza in min.
            print(f"Distanza: {distanza}, velocità: {velocita}, tempo_perc: {tempo_perc}")
            if (self._grafo.has_edge(u_nodo, v_nodo)):  # Se l'arco c'è già
                # Verifico se il tempo di percorrenza appena calcolato è minore di
                # di quello associato all'arco già presente, se così aggiorno
                if (self._grafo[u_nodo][v_nodo]["tempo"] > tempo_perc):
                    self._grafo[u_nodo][v_nodo]["tempo"] = tempo_perc
            else:  # Altrimenti lo aggiungo
                self._grafo.add_edge(u_nodo, v_nodo, tempo=tempo_perc)

        print(self._grafo)