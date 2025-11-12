
import uuid
from app.Acta.domain.entities import ActaEntity
from app.Acta.domain.repositories import ActaRepository
from app.Core.domain.entities import RegistroCalificadoEntity
from app.Core.domain.repositories import RegistroCalificadoRepository


class CrearActa:
    def __init__(self, acta_repo: ActaRepository, registro_repo: RegistroCalificadoRepository):
        self.acta_repo = acta_repo
        self.registro_repo = registro_repo

    def ejecutar(self, **data) -> ActaEntity:
        llave_maestra = f"LLAVE-{uuid.uuid4().hex[:8].upper()}"
        creado_por = data.pop("creado_por", None)  
        registro = RegistroCalificadoEntity(
            id=None,
            llave_documento=llave_maestra,
            tipo=data.get("tipo", "Posgrado"),
            snies=data.get("snies"),
        )
        self.registro_repo.save(registro)

        acta = ActaEntity(
            id=None,
            llave_maestra=llave_maestra,
            etiquetas_dinamicas=data,
            creado_por_id=creado_por.id if creado_por else None,  
        )
        return self.acta_repo.save(acta)