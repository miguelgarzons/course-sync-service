import uuid
from app.Biblioteca.domain.entities import BibliotecaEntity
from app.Biblioteca.domain.repositories import BibliotecaRepository
from app.Biblioteca.application.mappers import FormularioRecursosMapper
from app.Core.domain.entities import RegistroCalificadoEntity
from app.Core.domain.repositories import RegistroCalificadoRepository


class CrearBiblioteca:
    def __init__(self, biblioteca_repo: BibliotecaRepository, registro_repo: RegistroCalificadoRepository):
        self.biblioteca_repo = biblioteca_repo
        self.registro_repo = registro_repo

    def ejecutar(self, **data) -> BibliotecaEntity:
        """
        Crea una entidad Acta a partir del formulario recibido.
        Si el usuario no envía una llave_maestra, se genera automáticamente
        y se crea un nuevo RegistroCalificado asociado.
        """
      
        creado_por = data.pop("creado_por", None)  
        llave_maestra = data.pop("llave_maestra", None)  
        biblioteca = BibliotecaEntity(
                id=None,
                llave_maestra=llave_maestra,
                etiquetas_dinamicas=data,
                creado_por_id=creado_por.id if creado_por else None,  
            )
        return self.biblioteca_repo.save(biblioteca)