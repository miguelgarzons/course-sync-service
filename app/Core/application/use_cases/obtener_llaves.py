from app.Core.domain.repositories import RegistroCalificadoRepository


class ObtenerLlave:
    def __init__(self, registro_calificado_repo: RegistroCalificadoRepository):
        self.registro_calificado_repo = registro_calificado_repo

    def ejecutar(self) -> dict:
        acta = self.registro_calificado_repo.all()
        return acta
