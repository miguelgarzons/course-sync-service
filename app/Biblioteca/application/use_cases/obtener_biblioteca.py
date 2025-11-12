from app.Biblioteca.domain.entities import BibliotecaEntity
from app.Biblioteca.domain.repositories import BibliotecaRepository
from app.Biblioteca.application.mappers import FormularioRecursosMapper

class ObtenerBiblioteca:
    def __init__(self, biblioteca_repo: BibliotecaRepository):
        self.biblioteca_repo = biblioteca_repo

    def ejecutar(self, llave_id: str) ->BibliotecaEntity:
        biblioteca_entity = self.biblioteca_repo.find_by_llave(llave_id)
        return biblioteca_entity