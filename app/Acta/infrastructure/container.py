from dependency_injector import containers, providers
from app.Acta.infrastructure.repositories import ActaRepositoryImpl
from app.Core.infrastructure.repositories import RegistroCalificadoRepositoryImpl
from app.Acta.application.use_cases.crear_acta import CrearActa
from app.Acta.application.use_cases.obtener_acta import ObtenerActa


class ActaContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias del módulo Acta."""

    acta_repo = providers.Factory(ActaRepositoryImpl)
    registro_repo = providers.Factory(RegistroCalificadoRepositoryImpl)

    crear_acta = providers.Factory(
        CrearActa,
        acta_repo=acta_repo,
        registro_repo=registro_repo
    )

    obtener_acta = providers.Factory(
        ObtenerActa,
        acta_repo=acta_repo
    )
