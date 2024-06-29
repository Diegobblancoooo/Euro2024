from cargar_api import CargarApi
from entrada import Entrada
from producto import Producto
from estadio import Estadio
from factura import Factura
from restaurantes import Restaurante
from funciones_ayudante import seleccion


class NoEsVip(Exception):
    """
    Excepción personalizada para indicar que un cliente no tiene entradas VIP.
    """
    pass


def es_vip(cedula: int, api: CargarApi) -> list[Entrada]:
    """
    Verifica si un cliente tiene entradas VIP.

    Args:
        cedula (int): Cédula del cliente.
        api (CargarApi): Instancia de CargarApi para acceder a los datos.

    Returns:
        list[Entrada]: Lista de entradas VIP del cliente.

    Raises:
        NoEsVip: Si el cliente no tiene entradas VIP.
    """
    entradas = []
    for partido in api.partidos:
        for entrada in partido.entradas:
            if entrada.cliente.cedula == cedula and entrada.tipo == 'vip':
                entradas.append(entrada)
    if len(entradas) == 0:
        raise NoEsVip
    return entradas


def iniciar_compra(estadio: Estadio, edad: int) -> tuple[list[Producto], Restaurante]:
    """
    Inicia el proceso de compra en un restaurante dentro de un estadio.

    Args:
        estadio (Estadio): Estadio donde se encuentra el restaurante.
        edad (int): Edad del cliente.

    Returns:
        tuple[list[Producto], Restaurante]: Lista de productos deseados y el restaurante seleccionado.
    """
    if edad < 18:
        print("El cliente es menor de 18, no puede comprar bebidas alcohólicas. Por lo tanto no se mostrarán en el menú.")
    print(f"Restaurantes en el estadio {estadio.nombre}:")
    restaurante = seleccion(estadio.restaurantes)
    return restaurante.iniciar_compra(edad), restaurante


def compra_restaurante(api: CargarApi):
    """
    Realiza una compra en un restaurante para un cliente con entrada VIP.

    Args:
        api (CargarApi): Instancia de CargarApi para acceder a los datos.
    """
    while True:
        try:
            cedula = int(input("Ingrese la cédula del cliente: "))
            entradas = es_vip(cedula, api)
        except ValueError:
            print("Cédula inválida.")
            continue
        except NoEsVip:
            print("El cliente no tiene entrada VIP.")
            return
        break
    print("¿Con qué entrada desea comprar?")
    for i, entrada in enumerate(entradas):
        print(f"{i + 1}. {entrada.codigo} - {entrada.partido.estadio.nombre}")
    while True:
        try:
            estadio_num = int(input("Seleccione una opción: "))
            if estadio_num not in range(1, len(entradas) + 1):
                print("Opción inválida.")
                continue
            break
        except ValueError:
            print("Opción inválida.")
    entrada = entradas[estadio_num - 1]
    productos_deseados, restaurante = iniciar_compra(entrada.partido.estadio, entrada.cliente.edad)
    factura = Factura(entrada, productos_deseados, restaurante)
    entrada.compras.append(factura)
    entrada.cliente.compras.append(factura)


def buscar_restaurante(api: CargarApi, nombre: str) -> Restaurante:
    """
    Busca un restaurante por su nombre en todos los estadios.

    Args:
        api (CargarApi): Instancia de CargarApi para acceder a los datos.
        nombre (str): Nombre del restaurante a buscar.

    Returns:
        Restaurante: Restaurante encontrado.

    Raises:
        ValueError: Si el restaurante no se encuentra.
    """
    for estadio in api.estadios:
        for restaurante in estadio.restaurantes:
            if restaurante.nombre == nombre:
                return restaurante
    raise ValueError("Restaurante no encontrado.")