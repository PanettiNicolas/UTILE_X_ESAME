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

BONUS

DAY(data) / MONTH(data) / YEAR(data)           Preleva il valore del giorno/mese/anno da un dato di tipo data


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


#Esempio Week 11 (Artsmia)

class DAO:
    def __init__(self):
        pass

    @staticmethod
    def readObjects():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM objects"
        cursor.execute(query)
        for row in cursor: # row è un dizionario
            #result.append(Object(row["object_id"], row["object_name"]))
            result.append(Object(**row)) # ** fa l'unpacking del dizionario

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def readConnessioni(objects_dict): # Riceve la idMap degli Object
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT eo1.object_id AS o1, eo2.object_id AS o2, COUNT(*) AS peso
                    FROM exhibition_objects eo1, exhibition_objects eo2 
                    WHERE eo1.exhibition_id = eo2.exhibition_id 
                    AND eo1.object_id < eo2.object_id 
                    GROUP BY eo1.object_id, eo2.object_id"""
        cursor.execute(query)

        for row in cursor:
           o1 = objects_dict[row["o1"]]
           o2 = objects_dict[row["o2"]]
           peso = row["peso"]
           result.append(Connessione(o1, o2, peso))  #costruisce una Connessione

        cursor.close()
        conn.close()
        return result # lista di oggetti di tipo Connessione


#Esempio Week13 (Voli)

class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def getNodes(min, dizionarioAeroporti):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT tmp.id, tmp.IATA_CODE, count(*) as somma
                    FROM
                    (SELECT a.id, a.IATA_CODE, f.AIRLINE_ID, COUNT(*)   
                    FROM flights f, airports a
                    WHERE a.id = f.ORIGIN_AIRPORT_ID OR
                          a.id = f.DESTINATION_AIRPORT_ID 
                    GROUP BY a.id, a.IATA_CODE, f.AIRLINE_ID) AS tmp
                    GROUP BY tmp.id, tmp.IATA_CODE 
                    HAVING somma>= %s """

        cursor.execute(query, (min, ))

        for row in cursor:
            result.append(dizionarioAeroporti[row["id"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(dizionarioAeroporti):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, COUNT(*) AS voli
                   FROM flights f 
                   GROUP BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID """

        cursor.execute(query)

        for row in cursor:
            idPartenza = row["ORIGIN_AIRPORT_ID"]
            idAarrivo = row["DESTINATION_AIRPORT_ID"]
            aPartenza = dizionarioAeroporti[idPartenza]
            aArrivo = dizionarioAeroporti[idAarrivo]
            voli = row["voli"]
            result.append(Connessione(aPartenza, aArrivo, voli))


        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getEdgesConQueryComplessa(dizionarioAeroporti):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, COALESCE(t1.n, 0) + coalesce(t2.n, 0) as voli
                    from 
                    (SELECT f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , count(*) as n FROM flights f 
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) t1
                    left join 
                    (SELECT f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , count(*) as n FROM flights f 
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) t2
                    on t1.ORIGIN_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID and t1.DESTINATION_AIRPORT_ID = t2.ORIGIN_AIRPORT_ID
                    where t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID or t2.ORIGIN_AIRPORT_ID is null"""

        cursor.execute(query)
        for row in cursor:
            result.append(Connessione(dizionarioAeroporti[row["ORIGIN_AIRPORT_ID"]], dizionarioAeroporti[row["DESTINATION_AIRPORT_ID"]], row["voli"]))
        cursor.close()
        conn.close()
        return result
