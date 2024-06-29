import os


def generar_id(a: str, b: str, c: str) -> str:
    """
    Genera un ID usando las primeras 2 letras del nombre del equipo local, las primeras 2 letras del nombre del equipo visitante y la primera letra del nombre del estadio.

    Args:
        a (str): Nombre del equipo local.
        b (str): Nombre del equipo visitante.
        c (str): Nombre del estadio.

    Returns:
        str: ID generado en mayúsculas.
    """
    return f"{a[:2]}{b[:2]}{c[:1]}".upper()


def find_item(lista: list, condicion):
    """
    Busca un ítem en una lista que cumpla con una condición.

    Args:
        lista (list): Lista de ítems a buscar.
        condicion (function): Función que define la condición de búsqueda.

    Returns:
        item: Ítem que cumple con la condición o None si no se encuentra.
    """
    for item in lista:
        if condicion(item):
            return item
    return None


def menu_principal() -> str:
    """
    Imprime el menú principal y solicita una opción al usuario.

    Returns:
        str: Opción seleccionada por el usuario.
    """
    while True:
        print("\n----- Menú Principal -----")
        print("1. Comprar entrada")
        print("2. Validar boleto")
        print("3. Comprar en el restaurante (solo para VIP)")
        print("4. Ver estadísticas")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion not in ["1", "2", "3", "4", "5"]:
            print("\nOpción inválida. Intente de nuevo.")
            continue
        return opcion


def numero_perfecto(n: int) -> bool:
    """
    Determina si un número es perfecto.

    Args:
        n (int): Número a evaluar.

    Returns:
        bool: True si el número es perfecto, False en caso contrario.
    """
    suma = 0
    for i in range(1, n):
        if n % i == 0:
            suma += i
    return suma == n


def es_numero_vampiro(n: int) -> bool:
    """
    Determina si un número es vampiro.

    Args:
        n (int): Número a evaluar.

    Returns:
        bool: True si el número es vampiro, False en caso contrario.
    """
    def generate_combinations(s: str):
        if len(s) <= 1:
            return [s]
        else:
            combinations = []
            for i in range(len(s)):
                part1 = s[i]
                part2 = s[:i] + s[i+1:]
                for combo in generate_combinations(part2):
                    combinations.append(part1 + combo)
            return combinations

    n_str = str(n)
    if len(n_str) % 2 != 0:
        return False

    combinations = generate_combinations(n_str)
    for combo in combinations:
        mid = len(combo) // 2
        part1 = combo[:mid]
        part2 = combo[mid:]
        num1 = int(part1)
        num2 = int(part2)
        if num1 * num2 == n and not (num1 % 10 == 0 and num2 % 10 == 0):
            return True

    return False


def file_exists(archivos: list[str]) -> bool:
    """
    Verifica si todos los archivos en la lista existen.

    Args:
        archivos (list[str]): Lista de nombres de archivos.

    Returns:
        bool: True si todos los archivos existen, False en caso contrario.
    """
    for archivo in archivos:
        if not os.path.exists(archivo):
            return False
    return True


def seleccion(lista: list):
    """
    Permite seleccionar un ítem de una lista mediante la entrada del usuario.

    Args:
        lista (list): Lista de ítems a seleccionar.

    Returns:
        item: Ítem seleccionado de la lista.
    """
    for i, item in enumerate(lista):
        print(f"{i + 1}. {str(item)}")
    while True:
        try:
            seleccion = int(input("Seleccione una opción: "))
            if seleccion not in range(1, len(lista) + 1):
                print("Opción inválida. Intente de nuevo.")
                continue
            break
        except ValueError:
            print("Opción inválida. Intente de nuevo.")
    return lista[seleccion - 1]


def seleccion_multiple(lista: list):
    """
    Permite seleccionar múltiples ítems de una lista mediante la entrada del usuario.

    Args:
        lista (list): Lista de ítems a seleccionar.

    Returns:
        list: Lista de ítems seleccionados.
    """
    for i, item in enumerate(lista):
        print(f"{i + 1}. {str(item)}")
    while True:
        try:
            seleccion = [int(i) for i in input("Seleccione una opción, -1 para no seleccionar nada: ").split(", ")]
            if seleccion[0] == -1:
                return []
            if any([i not in range(1, len(lista) + 1) for i in seleccion]):
                print("Algun numero es inválido. Intente de nuevo.")
                continue
            break
        except ValueError:
            print("Opción inválida. Intente de nuevo.")
    return [lista[i - 1] for i in seleccion]