"""
----------------SQL e Estrazione dati dal DB------------

LETTURA DATI

SELECT *                 Seleziona tutte le colonne di una tabella

WHERE ...                Filtra i risultati in base ad una condizione  (Filtra i risultati PRIMA diu un eventuale aggregazione)

DISTINCT                 Elimina i duplicati dai risultati (Utilizzato nel select)

ORDERE BY                Ordina i risultati (ASC -> Crescente / DESC -> Decrescente)

LIMIT N                  Restituisce le prime N righe

AGGREGAZIONE E CALCOLO

COUNT()                  Conta il numero di righe

SUM(colonna)             Somma i valori di una colonna

AVG(colonna)             Calcola la media dei valori

GROUP BY                 Raggruppa le righe per una o più colonne   -->  !!!Necessario quando usi COUNT, SUM o AVG

HAVING                   Filtra i risultati DOPO l'aggregazione


Esempio creazione archi:

>SQL:   SELECT OriginID as v1, DestinationID as v2, COUNT(*) as peso
        FROM flights
        GROUP BY OriginID, DestinationID

>PYTHON:    for row in lista_archi:
                self._grafo.add_edge(row['v1'], row['v2'], weight=row['peso'])

Esempio "Self-join":

Si usa quando devi collegare due elementi che sono nella stessa tabella basandoti su una caratteristica comune (es. "collega due prodotti se sono stati comprati dallo stesso cliente")

>SQL:   SELECT t1.ProdottoID as p1, t2.ProdottoID as p2, COUNT(*) as num_comune
        FROM acquisti t1, acquisti t2
        WHERE t1.ClienteID = t2.ClienteID -- Stesso cliente
              AND t1.ProdottoID < t2.ProdottoID -- Evita duplicati e self-loop (A-A)
        GROUP BY t1.ProdottoID, t2.ProdottoID;

"""


#Esempio Lab10 (Hub e tratte)

""" select least(id_hub_origine, id_hub_destinazione ) as id_hub_a, greatest(id_hub_origine, id_hub_destinazione) as id_hub_b, avg(valore_merce)
    from spedizione
    group by id_hub_a, id_hub_b """

for row in cursor:
    tratta = Tratta(id_hub_A=row[0],
                    id_hub_B=row[1],
                    guadagno_medio=round(row[2], 2))

#L'accoppiata LEAST e GREATEST è utile per gestire i grafi non orientati --> Senza queste funzioni, se avessi una spedizione da Hub A a Hub B e una da Hub B a Hub A,
#                                                                            il database le vedrebbe come due righe distinte. Con questo trucco, le "unifichi"


#Esempio Lab13 (Geni e Cromosomi)

""" select g1.id, g2.id, i.correlazione
    from gene g1, gene g2, interazione i
    where g1.id = i.id_gene1 and g2.id = i.id_gene2    
          and g2.cromosoma != g1.cromosoma             
          and g2.cromosoma >0 and g1.cromosoma >0          
    group by g1.id, g2.id """

for row in cursor:
    result.append(row)


#Nel Model

edges = {}
for g1, g2, corr in self.listaGeniConnessi:                                 #Cicliamo sulla lista di geni connessi
    if (self.mappaCromosomi[g1], self.mappaCromosomi[g2]) not in edges:     #Se non esiste ancora il collegamento tra due cromosomi (a partire dall'interazione tra i geni <-- mappatura cromosomi)
        edges[(self.mappaCromosomi[g1], self.mappaCromosomi[g2])] = corr    #Allora creiamo il collegamento tra i due cromosomi e gli assegnamo come peso iniziale il peso della correlazione tra i due geni
    else:                                                                   #Altrimenti
        edges[(self.mappaCromosomi[g1], self.mappaCromosomi[g2])] += corr   #Sommiamo la correlazione dei due nuovi geni alla correlazione tra i geni già considerati tra i due cromosomi

for c, v in edges.items():           #Cicliamo sulle chiavi(tuple composte dagli id dei cromosomi collegati) e sui valori del dizionario edges
    self.edges.append((c[0], c[1], v))
    self.listaPesiArchi.append(v)    #Creiamo una lista con tutti i pesi degli archi che useremo dopo

self.G.add_weighted_edges_from(self.edges)   #Aggiunta lati al grafo