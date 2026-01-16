def get_sequenza_ottima(self, mese: int):
    """
    Calcola la sequenza ottimale di interventi nei primi 7 giorni
    :return: sequenza di nomi impianto ottimale
    :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
    """
    self.__sequenza_ottima = []
    self.__costo_ottimo = -1
    consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

    self.__ricorsione([], 1, None, 0, consumi_settimana)

    # Traduci gli ID in nomi
    id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
    sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
    return sequenza_nomi, self.__costo_ottimo


def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
    """ Implementa la ricorsione """
    # 🟢 Condizione Terminale
    if len(sequenza_parziale) == 7:  # 7 giorni schedulati
        if costo_corrente < self.__costo_ottimo or self.__costo_ottimo == -1:
            self.__costo_ottimo = costo_corrente
            self.__sequenza_ottima = sequenza_parziale[:]
        return

    for imp_id in consumi_settimana.keys():
        # 🔵 Calcola Parziale
        costo = consumi_settimana[imp_id][giorno - 1]
        if ultimo_impianto is not None and imp_id != ultimo_impianto:
            costo += 5
        sequenza_parziale.append(imp_id)

        # 🟡 Nessun filtro necessario quindi chiamo direttamente la ricorsione per il livello successivo
        self.__ricorsione(sequenza_parziale, giorno + 1, imp_id, costo_corrente + costo, consumi_settimana)

        # 🟣 Backtracking
        sequenza_parziale.pop()