from fastapi import APIRouter, Depends
from rrhh_common import Usuario, requiere_roles
from rrhh_common.crud import ROLES_LECTURA, router_crud
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import esquemas as e
from app import modelos as m
from app.db import obtener_sesion


def _crud(modelo, crear, parche, salida, prefijo, etiqueta, nombre, **extra):
    # Todos los catálogos se pueden buscar por nombre (?q=) para los combos del frontend.
    extra.setdefault("busqueda", ("nombre",))
    return router_crud(
        modelo=modelo,
        crear=crear,
        parche=parche,
        salida=salida,
        prefijo=prefijo,
        etiqueta=etiqueta,
        nombre=nombre,
        sesion=obtener_sesion,
        **extra,
    )


# Listados anidados del contrato (equivalentes a filtrar por el padre).
anidados = APIRouter()
leer = requiere_roles(*ROLES_LECTURA)


@anidados.get(
    "/paises/{pais_id}/departamentos",
    response_model=list[e.DepartamentoSalida],
    tags=["Países"],
    summary="Obtener departamentos por ID de país",
)
def departamentos_de_pais(
    pais_id: int, db: Session = Depends(obtener_sesion), _: Usuario = Depends(leer)
):
    consulta = select(m.Departamento).filter_by(pais_id=pais_id).order_by(m.Departamento.nombre)
    return db.scalars(consulta).all()


@anidados.get(
    "/departamentos/{departamento_id}/ciudades",
    response_model=list[e.CiudadSalida],
    tags=["Departamentos"],
    summary="Obtener ciudades por ID de departamento",
)
def ciudades_de_departamento(
    departamento_id: int, db: Session = Depends(obtener_sesion), _: Usuario = Depends(leer)
):
    consulta = select(m.Ciudad).filter_by(departamento_id=departamento_id).order_by(m.Ciudad.nombre)
    return db.scalars(consulta).all()


@anidados.get(
    "/ciudades/{ciudad_id}/barrios",
    response_model=list[e.BarrioSalida],
    tags=["Ciudades"],
    summary="Obtener barrios por ID de ciudad",
)
def barrios_de_ciudad(
    ciudad_id: int, db: Session = Depends(obtener_sesion), _: Usuario = Depends(leer)
):
    consulta = select(m.Barrio).filter_by(ciudad_id=ciudad_id).order_by(m.Barrio.nombre)
    return db.scalars(consulta).all()


routers = [
    _crud(
        m.TipoContrato,
        e.TipoContrato,
        e.TipoContratoUpdate,
        e.TipoContratoSalida,
        "/tipos-contrato",
        "Tipos de Contrato",
        "Tipo de contrato",
    ),
    _crud(
        m.Sector,
        e.Sector,
        e.SectorUpdate,
        e.SectorSalida,
        "/sectores",
        "Sectores",
        "Sector",
    ),
    _crud(
        m.Cargo,
        e.Cargo,
        e.CargoUpdate,
        e.CargoSalida,
        "/cargos",
        "Cargos",
        "Cargo",
        filtros={"sector_id": int},
    ),
    _crud(
        m.Pais,
        e.Pais,
        e.PaisUpdate,
        e.PaisSalida,
        "/paises",
        "Países",
        "País",
        busqueda=("nombre", "codigo_iso"),
    ),
    _crud(
        m.Departamento,
        e.Departamento,
        e.DepartamentoUpdate,
        e.DepartamentoSalida,
        "/departamentos",
        "Departamentos",
        "Departamento",
        filtros={"pais_id": int},
    ),
    _crud(
        m.Ciudad,
        e.Ciudad,
        e.CiudadUpdate,
        e.CiudadSalida,
        "/ciudades",
        "Ciudades",
        "Ciudad",
        filtros={"departamento_id": int},
    ),
    _crud(
        m.Barrio,
        e.Barrio,
        e.BarrioUpdate,
        e.BarrioSalida,
        "/barrios",
        "Barrios",
        "Barrio",
        filtros={"ciudad_id": int},
    ),
    anidados,
]
