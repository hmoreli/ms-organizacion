from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Numeric, String, true
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class TipoContrato(Base):
    __tablename__ = "tipo_contrato"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    duracion_dias: Mapped[int | None]


class Sector(Base):
    __tablename__ = "sector"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)


class Cargo(Base):
    __tablename__ = "cargo"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    # Guaraníes: sin decimales en la práctica, pero NUMERIC evita errores de redondeo.
    salario_base: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    sector_id: Mapped[int | None] = mapped_column(ForeignKey("sector.id"), index=True)


class Pais(Base):
    __tablename__ = "pais"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    codigo_iso: Mapped[str | None] = mapped_column(String(3), unique=True)
    gentilicio: Mapped[str | None] = mapped_column(String(100))
    # Código telefónico internacional sin "+" (Paraguay: 595).
    codigo_telefono: Mapped[str | None] = mapped_column(String(3))


class Departamento(Base):
    __tablename__ = "departamento"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    pais_id: Mapped[int] = mapped_column(ForeignKey("pais.id"), index=True)


class Ciudad(Base):
    __tablename__ = "ciudad"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    departamento_id: Mapped[int] = mapped_column(ForeignKey("departamento.id"), index=True)


class Barrio(Base):
    __tablename__ = "barrio"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    ciudad_id: Mapped[int] = mapped_column(ForeignKey("ciudad.id"), index=True)


class EntidadBancaria(Base):
    __tablename__ = "entidad_bancaria"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    # Las que dejan de operar se desactivan (los funcionarios pueden seguir apuntando a ellas).
    activo: Mapped[bool] = mapped_column(Boolean, server_default=true(), default=True)
