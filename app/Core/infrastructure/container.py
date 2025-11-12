from dependency_injector import containers, providers

from app.Core.application.use_cases.obtener_llaves import ObtenerLlave
from app.Core.infrastructure.repositories import RegistroCalificadoRepositoryImpl



class CoreContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias del módulo Acta."""

    registro_repo = providers.Factory(RegistroCalificadoRepositoryImpl)


    obtener_llave = providers.Factory(
        ObtenerLlave,
        registro_calificado_repo=registro_repo
    )
