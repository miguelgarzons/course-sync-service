from abc import ABC, abstractmethod

from app.Core.domain.entities import RegistroCalificadoEntity


class RegistroCalificadoRepository(ABC):
    """Interfaz abstracta del repositorio de DenominacionPrograma."""

    @abstractmethod
    def save(self, programa: RegistroCalificadoEntity) -> RegistroCalificadoEntity:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> RegistroCalificadoEntity:
        pass

    @abstractmethod
    def all(self) -> RegistroCalificadoEntity:
        pass

    @abstractmethod
    def exists_by_llave(self, id: int) -> bool:
        pass
