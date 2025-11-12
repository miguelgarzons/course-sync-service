from app.Acta.domain.entities import ActaEntity
from app.Acta.domain.repositories import ActaRepository

class ObtenerActa:
    def __init__(self, acta_repo: ActaRepository):
        self.acta_repo = acta_repo

    def ejecutar(self, llave_id: str) -> ActaEntity:
        acta = self.acta_repo.find_by_llave(llave_id)
        return acta
