from tests.conftest import CONSULTA, OPERADOR


def crear(cliente, ruta, datos):
    r = cliente.post(ruta, json=datos, headers=OPERADOR)
    assert r.status_code == 201, r.text
    return r.json()


def test_cargo_con_salario_como_numero(cliente):
    sector = crear(cliente, "/sectores", {"nombre": "Administración"})
    cargo = crear(
        cliente,
        "/cargos",
        {"nombre": "Contador", "salario_base": 4500000, "sector_id": sector["id"]},
    )
    assert cargo["salario_base"] == "4500000.00"
    assert cliente.get(f"/cargos?sector_id={sector['id']}", headers=CONSULTA).json() == [cargo]


def test_salario_negativo_es_invalido(cliente):
    r = cliente.post("/cargos", json={"nombre": "X", "salario_base": -1}, headers=OPERADOR)
    assert r.status_code == 422


def test_jerarquia_de_localizacion(cliente):
    py = crear(cliente, "/paises", {"nombre": "Paraguay", "codigo_iso": "PRY"})
    central = crear(cliente, "/departamentos", {"nombre": "Central", "pais_id": py["id"]})
    luque = crear(cliente, "/ciudades", {"nombre": "Luque", "departamento_id": central["id"]})
    crear(cliente, "/barrios", {"nombre": "Centro", "ciudad_id": luque["id"]})

    deps = cliente.get(f"/paises/{py['id']}/departamentos", headers=CONSULTA).json()
    assert [d["nombre"] for d in deps] == ["Central"]
    ciudades = cliente.get(f"/departamentos/{central['id']}/ciudades", headers=CONSULTA).json()
    assert [c["nombre"] for c in ciudades] == ["Luque"]
    barrios = cliente.get(f"/ciudades/{luque['id']}/barrios", headers=CONSULTA).json()
    assert [b["nombre"] for b in barrios] == ["Centro"]


def test_no_se_borra_un_pais_con_departamentos(cliente):
    py = crear(cliente, "/paises", {"nombre": "Paraguay"})
    crear(cliente, "/departamentos", {"nombre": "Central", "pais_id": py["id"]})
    assert cliente.delete(f"/paises/{py['id']}", headers=OPERADOR).status_code == 409


def test_departamento_con_pais_inexistente_da_409(cliente):
    r = cliente.post("/departamentos", json={"nombre": "X", "pais_id": 999}, headers=OPERADOR)
    assert r.status_code == 409


def test_patch_tipo_contrato(cliente):
    tc = crear(cliente, "/tipos-contrato", {"nombre": "Plazo fijo", "duracion_dias": 180})
    r = cliente.patch(f"/tipos-contrato/{tc['id']}", json={"duracion_dias": 365}, headers=OPERADOR)
    assert r.json() == {"id": tc["id"], "nombre": "Plazo fijo", "duracion_dias": 365}


def test_sin_token_401(cliente):
    assert cliente.get("/sectores").status_code == 401


def test_consulta_no_escribe(cliente):
    assert cliente.post("/sectores", json={"nombre": "X"}, headers=CONSULTA).status_code == 403


def test_rutas_del_contrato_existen(cliente):
    rutas = cliente.get("/openapi.json").json()["paths"]
    esperadas = {
        "/tipos-contrato",
        "/tipos-contrato/{id}",
        "/sectores",
        "/sectores/{id}",
        "/cargos",
        "/cargos/{id}",
        "/paises",
        "/paises/{id}",
        "/paises/{pais_id}/departamentos",
        "/departamentos",
        "/departamentos/{id}",
        "/departamentos/{departamento_id}/ciudades",
        "/ciudades",
        "/ciudades/{id}",
        "/ciudades/{ciudad_id}/barrios",
        "/barrios",
        "/barrios/{id}",
    }
    assert esperadas <= set(rutas)


def test_busqueda_en_catalogos(cliente):
    for nombre, iso in (("Paraguay", "PRY"), ("Argentina", "ARG"), ("Uruguay", "URY")):
        crear(cliente, "/paises", {"nombre": nombre, "codigo_iso": iso})
    assert [p["nombre"] for p in cliente.get("/paises?q=guay", headers=CONSULTA).json()] == [
        "Paraguay",
        "Uruguay",
    ]
    assert [p["nombre"] for p in cliente.get("/paises?q=arg", headers=CONSULTA).json()] == [
        "Argentina"
    ]


def test_entidades_bancarias(cliente):
    itau = crear(cliente, "/entidades-bancarias", {"nombre": "Banco Itaú"})
    assert itau["activo"] is True
    crear(cliente, "/entidades-bancarias", {"nombre": "Banco Familiar", "activo": False})
    activas = cliente.get("/entidades-bancarias?activo=true", headers=CONSULTA).json()
    assert [b["nombre"] for b in activas] == ["Banco Itaú"]
    r = cliente.post("/entidades-bancarias", json={"nombre": "Banco Itaú"}, headers=OPERADOR)
    assert r.status_code == 409


def test_codigo_telefonico_del_pais(cliente):
    py = crear(cliente, "/paises", {"nombre": "Paraguay", "codigo_telefono": "595"})
    assert py["codigo_telefono"] == "595"
    r = cliente.post("/paises", json={"nombre": "X", "codigo_telefono": "+595"}, headers=OPERADOR)
    assert r.status_code == 422
