from entrada import Entrada
from partido import Partido
from cliente import Cliente
from cargar_api import CargarApi
from funciones_partidos import buscar_partidos


def comprar_entrada(api: CargarApi, clientes: list[Cliente]) -> Cliente:
    """
    Permite al usuario comprar una entrada para un partido.

    Args:
        api (CargarApi): Instancia de CargarApi para acceder a los datos.
        clientes (list[Cliente]): Lista de clientes existentes.

    Returns:
        Cliente: El cliente que compró la entrada.
    """
    while True:
        try:
            cedula_cliente = int(input("Ingrese la cédula del cliente: "))
        except ValueError:
            print("La cédula es inválida, debe ser un número entero. Intente de nuevo.")
            continue
        break

    cliente = cliente_existe(cedula_cliente, clientes)
    if cliente is None:
        nombre_cliente = input("Ingrese el nombre del cliente: ")
        while True:
            try:
                edad_cliente = int(input("Ingrese la edad del cliente: "))
            except ValueError:
                print("La edad es inválida, debe ser un número entero. Intente de nuevo.")
                continue
            break
        cliente = Cliente(nombre_cliente, cedula_cliente, edad_cliente)
    print("\nSeleccione el partido:")
    partido = buscar_partidos(api)
    while True:
        tipo_entrada = input("Ingrese el tipo de entrada (General: 35$ | VIP: 75$): ").lower()
        if tipo_entrada not in ["general", "vip"]:
            print("Tipo de entrada inválida. Intente de nuevo.")
            continue
        break
    asiento = partido.modificar_asientos(tipo_entrada == "vip")
    codigo = f"{asiento} {partido.id}"
    print(f"El código de su boleto es: {codigo}")
    entrada = Entrada(tipo_entrada, partido, asiento, cliente, codigo)
    partido.registrar_entrada(entrada)
    cliente.entradas.append(entrada)
    return cliente


def validar_entrada(api: CargarApi) -> None:
    """
    Valida una entrada cambiando su estado a validado si el código es correcto.

    Args:
        api (CargarApi): Instancia de CargarApi para acceder a los datos.
    """
    codigo = input("Ingrese el código de la entrada: ")
    for partido in api.partidos:
        for entrada in partido.entradas:
            if entrada.codigo == codigo:
                if entrada.validado:
                    print("La entrada ya ha sido validada.")
                else:
                    entrada.validado = True
                    print("Entrada validada.")
                    partido.asistencia += 1


def cliente_existe(cedula_cliente: int, clientes: list[Cliente]) -> Cliente or None:
    """
    Verifica si un cliente ya existe en la lista de clientes.

    Args:
        cedula_cliente (int): Cédula del cliente a verificar.
        clientes (list[Cliente]): Lista de clientes existentes.

    Returns:
        Cliente or None: El cliente si existe, None en caso contrario.
    """
    for cliente in clientes:
        if cliente.cedula == cedula_cliente:
            return cliente
    return None
