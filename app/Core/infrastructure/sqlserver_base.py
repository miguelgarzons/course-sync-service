from django.db import models

class SQLServerBaseModel(models.Model):
    """
    Clase base para modelos que se conectan a SQL Server.
    Evita migraciones y facilita herencia.
    """
    class Meta:
        abstract = True
        managed = False
