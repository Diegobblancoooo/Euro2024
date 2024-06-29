from cargar_api import CargarApi
from partido import Partido
from funciones_ayudante import seleccion


def buscar_partidos(api: CargarApi) -> Partido:
    """
    Permite al usuario buscar partidos por país, estadio o fecha.

    Args:
        api (CargarApi): Instancia de CargarApi para acceder a los datos.

    Returns:
        Partido: Partido seleccionado por el usuario.
    """
    print("1. Buscar partidos por país")
    print("2. Buscar partidos por estadio")
    print("3. Buscar partidos por fecha")
    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        return buscar_por_pais(api)
    elif opcion == "2":
        return buscar_por_estadio(api)
    elif opcion == "3":
        return buscar_por_fecha(api)


def buscar_por_pais(api: CargarApi) -> Partido:
    """
    Busca partidos por el nombre del país.

    Args:
        api (CargarApi): Instancia de CargarApi para acceder a los datos.

    Returns:
        Partido: Partido seleccionado por el usuario.
    """
    nombre_pais = seleccion(api.equipos).nombre
    partidos_pais = [partido for partido in api.partidos if partido.equipo_local.nombre == nombre_pais or partido.equipo_visitante.nombre == nombre_pais]
    print(f"\nPartidos en {nombre_pais}:")
    return seleccion(partidos_pais)


def buscar_por_estadio(api: CargarApi) -> Partido:
    """
    Busca partidos por el nombre del estadio.

    Args:
        api (CargarApi): Instancia de CargarApi para acceder a los datos.

    Returns:
        Partido: Partido seleccionado por el usuario.
    """
    nombre_estadio = seleccion(api.estadios).nombre
    partidos_estadio = [partido for partido in api.partidos if partido.estadio.nombre == nombre_estadio]
    print(f"\nPartidos en el estadio {nombre_estadio}")
    return seleccion(partidos_estadio)


def buscar_por_fecha(api: CargarApi) -> Partido:
    """
    Busca partidos por la fecha.

    Args:
        api (CargarApi): Instancia de CargarApi para acceder a los datos.

    Returns:
        Partido: Partido seleccionado por el usuario.
    """
    fechas = sorted({partido.fecha for partido in api.partidos}, key=lambda x: x[4:])
    fecha = seleccion(fechas)
    partidos_fecha = [partido for partido in api.partidos if partido.fecha.startswith(fecha)]
    print(f"\nPartidos el día {fecha}")
    return seleccion(partidos_fecha)


def buscar_por_id(api: CargarApi, partido_id: str) -> Partido or None:
    """
    Busca un partido por su ID.

    Args:
        api (CargarApi): Instancia de CargarApi para acceder a los datos.
        partido_id (str): ID del partido a buscar.

    Returns:
        Partido or None: Partido encontrado o None si no se encuentra.
    """
    for partido in api.partidos:
        if partido.id == partido_id:
            return partido
    return None