"""
--------------------Flet e Interfaccia Utente----------------------

L'Interfaccia Utente si costruisce aggiungendo controlli (widget) alla pagina grazie alla libreria Flet

!!! La libreria da importare è: import flet as ft
"""

#--------------------Struttura della pagina-------------------------

page.update()                      #Ricarica la UI per mostrare le moddifiche (Fondamentale per attuare i cambiamenti)

#--------------------Gestione Eventi e Reattività (Controller <-> View)-------------

on_click             #Innesca l'azione al click   -->   Es. utilizzo: avviare la creazione del grafo/il calcolo ricorsivo

on_change            #Rileva ogni minima modifica   -->   Es. utilizzo: filtrare i risultati in tempo reale

e.control.value      #Recupera il valore attuale del componente che ha scatenato l'evento   -->  Es. utilizzo: leggere quale nodo è stato selezionato nel dropdown

#----------------------Input e Selezione (Controlli ATTIVI)-------------------

ft.ElevatedButton    #Metodi chiave: on_click

ft.TextField         #Metodi chiave: on_change

ft.Dropdown          #Metodi chiave: options, on_change
ft.Dropdown.options.append(ft.dropdown.Option(key, text))            #Aggiunta opzione al dd


#------------------Output e Visualizzazione (Controlli PASSIVI)-------------

ft.Text              #Metodi chiave: controls.append, clean()        Mostra mesasggi brevi <-- Risultati brevi

ft.ListView          #Metodi chiave: controls.append, clean()        Mostra liste <-- Risultati lunghi




#Esempio Lab09 (Regioni e Tour)

class Controller:
    def __init__(self, view: View, model: Model):
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        self.regione_selezionata = None
        self.durata = None
        self.costo = None

    def popola_dropdown_regione(self):
        """Popola il menu a tendina delle regioni."""
        self._view.dd_regione.options.clear()

        regioni = self._model.load_regioni() # Ogni regione (id, nome_regione)

        if regioni:
            for regione in sorted(regioni):
                self._view.dd_regione.options.append(ft.dropdown.Option(key=regione.id,text=regione.nome))
        else:
            self._view.show_alert("Errore nel caricamento delle regioni.")

        self._view.update()

    def on_regione_change(self, e):
        """Aggiorna la regione selezionata e salva il valore."""
        self.regione_selezionata = e.control.value




class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "Lab09"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None

    #...

    def load_interface(self):
        #...
        # Regioni

        self.dd_regione = ft.Dropdown(
            label="Regione",
            menu_height=150,
            width=200,
            hint_text="Selezionare una regione",
            on_change=self.controller.on_regione_change
        )
        self.controller.popola_dropdown_regione()

        #...

#Esempio Lab07 (Musei Torino)

class Controller:
    def __init__(self, view: View, model: Model):
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        self.museo_selezionato = None
        self.epoca_selezionata = None

    # POPOLA DROPDOWN
    def popola_dropdown_musei(self):
        """Popola il menu a tendina dei musei."""
        self._view.dropdown_museo.options.clear()
        self._view.dropdown_museo.options.append(ft.dropdown.Option(None, "Nessun Filtro"))

        musei = self._model.get_musei()

        if musei:
            for museo in musei:
                self._view.dropdown_museo.options.append(ft.dropdown.Option(museo.nome))
        else:
            self._view.show_alert("Errore nel caricamento dei musei.")

        self._view.update()

    def popola_dropdown_epoche(self):
        """Popola il menu a tendina con TUTTE le epoche disponibili nel DB."""
        self._view.dropdown_epoca.options.clear()
        self._view.dropdown_epoca.options.append(ft.dropdown.Option(None, "Nessun Filtro"))

        epoche = self._model.get_epoche()

        if epoche:
            for epoca in epoche:
                self._view.dropdown_epoca.options.append(ft.dropdown.Option(epoca))
        else:
            self._view.show_alert("Errore nel caricamento delle epoche.")

        self._view.update()


    #Callback dropdown
    def on_museo_change(self, e):
        """Aggiorna il museo selezionato e salva il valore."""
        valore = e.control.value
        self.museo_selezionato = None if valore == "Nessun Filtro" else valore

    def on_epoca_change(self, e):
        """Aggiorna l'epoca selezionata e salva il valore."""
        valore = e.control.value
        self.epoca_selezionata = None if valore == "Nessun Filtro" else valore



class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "Lab07"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None
        #...

    def load_interface(self):
        #...

        # Dropdown musei
        self.dropdown_museo = ft.Dropdown(
            label="Museo",
            width=400,
            options=[ft.dropdown.Option(key="None", text="Nessun Filtro")],
            on_change=self.controller.on_museo_change  # Callback collegata
        )
        self.controller.popola_dropdown_musei()

        # Dropdown epoca
        self.dropdown_epoca = ft.Dropdown(
            label="Epoca",
            width=220,
            options=[ft.dropdown.Option(key="None", text="Nessun Filtro")],
            on_change=self.controller.on_epoca_change  # Callback collegata
        )
        self.controller.popola_dropdown_epoche()
