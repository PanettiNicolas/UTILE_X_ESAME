

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



     # --- VIEW ---
 # Dropdown epoca
        self.dropdown_epoca = ft.Dropdown(
            label="Epoca",
            width=220,
            options=[ft.dropdown.Option(key="None", text="Nessun Filtro")],
            on_change=self.controller.on_epoca_change  # Callback collegata
        )
        self.controller.popola_dropdown_epoche()


# CALLBACKS DROPDOWN
    def on_museo_change(self, e):
        """Aggiorna il museo selezionato e salva il valore."""
        valore = e.control.value
        self.museo_selezionato = None if valore == "Nessun Filtro" else valore


    def mostra_artefatti(self, e):
        """Mostra gli artefatti filtrati per museo e/o epoca (filtri opzionali)."""
        museo = self.museo_selezionato
        epoca = self.epoca_selezionata

        self._view.lista_artefatti.controls.clear()
        lista_artefatti = self._model.get_artefatti_filtrati(museo, epoca)

        if lista_artefatti is None:
            self._view.show_alert("Errore di connessione al database.")
        elif len(lista_artefatti) == 0:
            self._view.show_alert("Nessun artefatto trovato per i criteri selezionati")
        else:
            for artefatto in lista_artefatti:
                self._view.lista_artefatti.controls.append(ft.Text(f"{artefatto}"))

        self._view.update()