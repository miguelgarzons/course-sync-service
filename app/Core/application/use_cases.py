import random
import uuid
from datetime import datetime

from app.Core.domain.entities import RegistroCalificadoEntity
from app.Core.domain.repositories import RegistroCalificadoRepository


class CrearLLaveMaestra:
    def __init__(self, repo: RegistroCalificadoRepository):
        self.repo = repo

    def ejecutar(self) -> RegistroCalificadoEntity:
        llave_documento = f"LLAVE-{uuid.uuid4().hex[:8].upper()}"
        tipo = random.choice(["Resolución", "Acuerdo", "Decreto", "Certificación"])
        snies = f"SNIES-{random.randint(10000, 99999)}"
        programa = RegistroCalificadoEntity(
            id=None,
            llave_documento=llave_documento,
            tipo=tipo,
            snies=snies,
            creado_en=datetime.now(),
            actualizado_en=datetime.now(),
        )

        return self.repo.save(programa)
