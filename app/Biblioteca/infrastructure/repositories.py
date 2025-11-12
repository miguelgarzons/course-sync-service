# app/Acta/infrastructure/repositories.py

import uuid
from app.Core.infrastructure.models import RegistroCalificado
from app.Biblioteca.infrastructure.models import Biblioteca
from app.Biblioteca.domain.entities import BibliotecaEntity
from app.Biblioteca.domain.repositories import BibliotecaRepository
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
class BibliotecaRepositoryImpl(BibliotecaRepository):
    def save(self, biblioteca_entity: BibliotecaEntity) -> BibliotecaEntity:
        """
        Guarda una Acta en la base de datos.
        Convierte llave_maestra (string) en instancia del modelo RegistroCalificado.
        """

        registro_model = RegistroCalificado.objects.get(llave_documento=biblioteca_entity.llave_maestra)

        acta_model = Biblioteca.objects.create(
            llave_maestra=registro_model,
            etiquetas_dinamicas=biblioteca_entity.etiquetas_dinamicas
        )

        return BibliotecaEntity(
            id=acta_model.id,
            llave_maestra=acta_model.llave_maestra.llave_documento,
            etiquetas_dinamicas=acta_model.etiquetas_dinamicas,
            creado_en=acta_model.creado_en,
            actualizado_en=acta_model.actualizado_en
        )
        

    def find_by_id(self, id: int) -> BibliotecaEntity:
        """Recupera una entidad Acta desde la base de datos."""
        try:
            model = Biblioteca.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise ValueError(f"No existe un acta con id {id}")
        return BibliotecaEntity(
            id=model.id,
            llave_maestra=model.llave_maestra,
            etiquetas_dinamicas=model.etiquetas_dinamicas,
            creado_en=model.creado_en,
            actualizado_en=model.actualizado_en,
        )

    def find_by_llave(self, llave_id: str) -> BibliotecaEntity:
        """Recupera una entidad Acta desde la base de datos usando la llave maestra."""
        try:
            model = Biblioteca.objects.get(llave_maestra__llave_documento=llave_id)
        except Biblioteca.DoesNotExist:
           raise NotFound(f"No existe un acta con llave {llave_id}")
        return BibliotecaEntity(
            id=model.id,
            llave_maestra=model.llave_maestra,
            etiquetas_dinamicas=model.etiquetas_dinamicas,
            creado_en=model.creado_en,
            actualizado_en=model.actualizado_en,
        )