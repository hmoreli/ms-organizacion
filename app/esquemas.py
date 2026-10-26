"""Esquemas del contrato contrato/openapi.yaml.

Agregados respecto al contrato: `codigo_iso` y `gentilicio` en Pais (vienen
del ScriptBD.sql), ambos opcionales.
"""

from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

# NUMERIC(14,2): entra como número o texto y sale como texto ("4500000.00") para no
# perder precisión en guaraníes.
Monto = Annotated[Decimal, Field(ge=0, max_digits=14, decimal_places=2)]
Nombre = Annotated[str, Field(min_length=1, max_length=100)]


class _Salida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TipoContrato(BaseModel):
    nombre: Nombre
    duracion_dias: int | None = Field(None, ge=1)


class TipoContratoUpdate(BaseModel):
    nombre: Nombre | None = None
    duracion_dias: int | None = Field(None, ge=1)


class TipoContratoSalida(TipoContrato, _Salida):
    pass


class Sector(BaseModel):
    nombre: Nombre


class SectorUpdate(BaseModel):
    nombre: Nombre | None = None


class SectorSalida(Sector, _Salida):
    pass


class Cargo(BaseModel):
    nombre: Nombre
    salario_base: Monto
    sector_id: int | None = None


class CargoUpdate(BaseModel):
    nombre: Nombre | None = None
    salario_base: Monto | None = None
    sector_id: int | None = None


class CargoSalida(Cargo, _Salida):
    pass


class Pais(BaseModel):
    nombre: Nombre
    codigo_iso: str | None = Field(None, min_length=2, max_length=3)
    gentilicio: str | None = Field(None, max_length=100)


class PaisUpdate(BaseModel):
    nombre: Nombre | None = None
    codigo_iso: str | None = Field(None, min_length=2, max_length=3)
    gentilicio: str | None = Field(None, max_length=100)


class PaisSalida(Pais, _Salida):
    pass


class Departamento(BaseModel):
    nombre: Nombre
    pais_id: int


class DepartamentoUpdate(BaseModel):
    nombre: Nombre | None = None
    pais_id: int | None = None


class DepartamentoSalida(Departamento, _Salida):
    pass


class Ciudad(BaseModel):
    nombre: Nombre
    departamento_id: int


class CiudadUpdate(BaseModel):
    nombre: Nombre | None = None
    departamento_id: int | None = None


class CiudadSalida(Ciudad, _Salida):
    pass


class Barrio(BaseModel):
    nombre: Nombre
    ciudad_id: int


class BarrioUpdate(BaseModel):
    nombre: Nombre | None = None
    ciudad_id: int | None = None


class BarrioSalida(Barrio, _Salida):
    pass
