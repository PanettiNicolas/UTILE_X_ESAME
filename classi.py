"""
-----------------------------Classi--------------------------------

!!! Importante importare: from dataclasses import dataclass

@dataclass
class Classe:
    attributo_1 : tipo
    atrributo_2 : tipo
    attributo_3 : tipo = valore_default

    def __str__(self):                                   <---  Definisce come l'oggetto viene stampato
        return f"{self.attributo_1} {self.attributo_2}"

    def __hash__(self):                                  <--  Permette di usare l'oggetto come chiave nei dizionari o nei set (Fonfamentale nei GRAFI)
        return hash(self.attributo_1)

    def __eq__(self, other):                            <-- Permette di verificare quando due oggetti sono uguali
        if not isinstance(other, Classe):               <-- Verifica che il confronto avvenga tra due oggetti dello stesso tipo
            return False
        return self.attributo_1 == other.attributo_1

    def calcola_qualcosa(self):
        return calcolo


>DAO:       for row in cursor:
                risultato.append(Gene(row['id'], row['nome'], row['cromosoma']))

>MODEL:     Se hai definito __hash__ e __eq__, puoi fare:

            self._grafo.add_node(gene_oggetto)

            !!! NetworkX userà l'oggetto intero come chiave del nodo!

>VIEW:      Se hai definito __str__, il dropdown mostrerà il nome del gene automaticamente

            for g in lista_geni:
                self._view.dd_geni.options.append(ft.dropdown.Option(data=g, text=str(g)))
"""



#Esempio Lab08 (Gestione Energia)

@dataclass()
class Impianto:
    id: int
    nome: str
    indirizzo: str

    # RELAZIONI (1:N)
    lista_consumi: list = None

    def get_consumi(self):
        """ Aggiorna e Restituisce la lista di consumi (self.lista_consumi) associati all'impianto"""
        if self.lista_consumi is None:
            self.lista_consumi = ConsumoDAO.get_consumi(self.id)
        return self.lista_consumi

    def __eq__(self, other):
        return isinstance(other, Impianto) and self.id == other.id

    def __str__(self):
        return f"{self.id} | {self.nome} | Indirizzo: {self.indirizzo}"

    def __repr__(self):
        return f"{self.id} | {self.nome} | Indirizzo: {self.indirizzo}"