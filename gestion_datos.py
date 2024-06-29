import os
from cliente import Cliente
from entrada import Entrada
from factura import Factura
from producto import Producto
from cargar_api import CargarApi
from funciones_partidos import buscar_por_id
from funciones_ayudante import file_exists
from funciones_restaurantes import buscar_restaurante


def guardar_datos(datos: list[Cliente]):
    """
    Guarda los datos de los clientes en un archivo.

    Args:
        datos (list[Cliente]): Lista de clientes a guardar.
    """
    if len(datos) > 0:
        if os.path.exists("datos_clientes.txt"):
            os.remove("datos_clientes.txt")
    with open("datos_clientes.txt", "a") as file:
        for cliente in datos:
            file.write(str(cliente.__dict__()))
            file.write("\n")
    print("Datos guardados con éxito.")


def cargar_datos(api: CargarApi) -> list[Cliente]:
    """
    Carga los datos de los clientes desde un archivo.

    Args:
        api (CargarApi): Instancia de CargarApi para acceder a los datos.

    Returns:
        list[Cliente]: Lista de clientes cargados desde el archivo.
    """
    clientes = []
    if not file_exists(["datos_clientes.txt"]):
        return clientes
    with open("datos_clientes.txt", "r") as file:
        for line in file:
            datos = eval(line)
            cliente = Cliente(datos["nombre"], datos["cedula"], datos["edad"])
            entradas = datos["entradas"]
            partidos = [buscar_por_id(api, entrada["partido"]) for entrada in datos["entradas"]]
            for i, entrada in enumerate(entradas):
                partidos[i].modificar_asientos_(entrada["tipo"] == "vip", entrada["asiento"])
                partidos[i].asistencia += 1 if entrada["validado"] else 0
                entra = Entrada(entrada["tipo"], partidos[i], entrada["asiento"], cliente, entrada["codigo"], True)
                if entrada["validado"]:
                    entra.validado = True
                for compras in entrada["compras"]:
                    productos = [Producto(producto["nombre"], producto["cantidad"], producto["precio"], producto["stock"], producto["adicional"]) for producto in compras["productos"]]
                    restaurante = buscar_restaurante(api, compras["restaurante"])
                    entra.compras.extend([Factura(entra, productos, restaurante, True)])
                partidos[i].entradas.append(entra)
                cliente.entradas.append(entra)
            clientes.append(cliente)
    return clientes

