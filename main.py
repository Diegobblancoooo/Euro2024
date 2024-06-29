from cargar_api import CargarApi
from funciones_ayudante import menu_principal
from funciones_entradas import comprar_entrada, validar_entrada
from funciones_restaurantes import compra_restaurante
from estadisticas import Estadisticas
from gestion_datos import guardar_datos, cargar_datos


def main() -> None:
    api = CargarApi()
    clientes = []
    clientes.extend(cargar_datos(api))
    while True:
        opcion = menu_principal()
        if opcion == "1":
            clientes.append(comprar_entrada(api, clientes))
        elif opcion == "2":
            validar_entrada(api)
        elif opcion == "3":
            compra_restaurante(api)
        elif opcion == "4":
            Estadisticas(api)
        elif opcion == "5":
            guardar_datos(clientes)
            break


if __name__ == "__main__":
    main()
