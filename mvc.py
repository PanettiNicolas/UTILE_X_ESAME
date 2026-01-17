"""
-----------------Struttura MVC + DAO----------------

>MODEL: logica e dati

        Funzioni: - Rappresenta la struttura dati
                  - Si occupa di gestire lo stato dell'applicazione
                  - Interagisce con il database (DAO)

        Collegato a DAO e Controller

>VIEW: l'interfaccia con Flet

        Funzioni: - Rappresenta l'interfaccia utente (UI)
                  - Riceve i dati elaboorati dal Model attraverso il Controller

        Collegato a Controller

>CONTROLLER: l'intermediario

             Funzioni: - Funziona da intermediario tra Model e View
                       - Gestisce la logica del flusso dell'applicazione:
                         riceve gli input dalla View, li convalida, interroga il Model e aggiorna la View con i risultati

            Collegato a Model e View


>DAO: è il responsabile esclusivo della persistenza dei dati.

     Funzione: - Preleva i dati dal DB, traducendo rihge di tabelle SQL in oggetti Python

     Collegato a Model

     !!! Il DAO non viene MAI chiamato direttamente dalla View o dal Controller MA solo dal Model


Riassunto comunicazione componenti:

Database <-> DAO <-> Model <-> Controller <-> View


"""

#-------------Struttura standard INTERROGAZIONE DAO--------------

from database.DB_connect import DBConnect
from model.connessione import Conessione

class DAO:
    @staticmethod
    def get_dati_filtrati(parametro_filtro):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        result = [] / {}       #In base a se il risultato sia una lista o un dizionario
        
        if cnx is None:         #Verifica connessione
            print("Errore di connessione al database")
            return None
        
        query = """ query con filtro in %s """
        
        try:                    #Verifica riuscita query
            cursor.execute(query, (parametro_filtro,))
            
            for row in cursor:
                result.append(row)
                
        except Exception as e:
            print(f"Errore durante lo svolgimento della query: {e}")
            
        finally:
            cursor.close()
            cnx.close()
            
        return result
        


#--------------Struttura standard MODEL-------------

from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        #Attrributi model UTILIZZATI all'intterno della classe
        #Funzioni load_ che carichino gli attributi al Model prelevati dal DB
        #!!! Gli attributi utilizzati SOLO nel Controller possono essere passati direttamente attraverso le funzioni get_
        self.lista_attributi = []

    def get_attributi(self):
        return DAO.get_attributi()         #<--- Nel Controller

    def load_attributi(self):
        self.lista_attributi = DAO.get_attributi()       #<--- Nel Model

    def crea_grafo(self):
        #Vedi file su Grafi
        pass

    def ricorsione(self):
        #Vedi file su Ricorsione
        pass


#---------------Struttura standard CONTROLLER--------------

class Controller:
    def __init__(self):
        #Riferimenti ai componenti MVC
        self._view = view
        self.model = model

        #Eventuali attributi del controller


    def handle_bottone(self, e):
        #Vedi file su Flet
        pass

