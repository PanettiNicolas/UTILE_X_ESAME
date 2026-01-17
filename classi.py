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