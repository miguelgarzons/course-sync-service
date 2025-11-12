from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RegistroCalificadoEntity:
    """
    Entidad de dominio pura que representa un registro calificado.
    """

    id: Optional[int]
    llave_documento: str
    tipo: str
    snies: str
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None

    def resumen(self) -> str:
        return f"{self.tipo}: {self.llave_documento} (SNIES {self.snies})"
