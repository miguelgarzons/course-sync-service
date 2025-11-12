from abc import ABC, abstractmethod

from app.Biblioteca.domain.entities import BibliotecaEntity


class BibliotecaRepository(ABC):
    @abstractmethod
    def save(
        self, programa: BibliotecaEntity
    ) -> BibliotecaEntity:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> BibliotecaEntity:
        pass

    @abstractmethod
    def find_by_llave(self, id: int) -> BibliotecaEntity:
        pass

