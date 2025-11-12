from dependency_injector import containers, providers
from app.Acta.infrastructure.container import ActaContainer
from app.Biblioteca.infrastructure.container import BibliotecaContainer
from app.Core.infrastructure.container import CoreContainer

class ApplicationContainer(containers.DeclarativeContainer):
    """Contenedor global de la aplicación."""

    acta = providers.Container(ActaContainer)
    biblioteca = providers.Container(BibliotecaContainer)
    core = providers.Container(CoreContainer)
