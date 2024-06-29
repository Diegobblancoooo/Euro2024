from producto import Producto
from funciones_ayudante import seleccion_multiple


class Restaurante:
    """
    Representa un restaurante con su nombre y lista de productos.

    Attributes:
        nombre (str): Nombre del restaurante.
        productos (list): Lista de productos ofrecidos por el restaurante.
    """

    def __init__(self, nombre: str, productos: list[dict]):
        """
        Inicializa una instancia de la clase Restaurante.

        Args:
            nombre (str): Nombre del restaurante.
            productos (list[dict]): Lista de productos en formato de diccionario.
        """
        self.nombre = nombre
        self.productos = []
        self.registrar_productos(productos)

    def registrar_productos(self, productos: list[dict]):
        """
        Registra los productos en la lista de productos del restaurante.

        Args:
            productos (list[dict]): Lista de productos en formato de diccionario.
        """
        for producto in productos:
            self.productos.append(Producto(producto["name"], producto["quantity"], float(producto["price"]), producto["stock"], producto["adicional"]))

    def productos_por_precio(self, edad: int) -> list[Producto]:
        """
        Busca productos por rango de precio.

        Args:
            edad (int): Edad del cliente.

        Returns:
            list[Producto]: Lista de productos dentro del rango de precio especificado.
        """
        productos_seleccionados = []
        while True:
            try:
                rango = input("Ingrese el rango de precios separados por un espacio: ")
                rango = [float(i) for i in rango.split(" ")]
                if len(rango) != 2:
                    raise ValueError
                if rango[0] > rango[1]:
                    raise ValueError
                lp = [producto for producto in self.productos if rango[0] < producto.precio < rango[1]]
                if edad < 18:
                    lp = [producto for producto in lp if not producto.alcoholic]
                productos_seleccionados.extend(seleccion_multiple(lp))
                sn = input("Desea buscar otros productos por rango de precios? (s/n): ")
                if sn == "s":
                    continue
                else:
                    return productos_seleccionados
            except ValueError:
                print("Rango inválido. Debe ser dos números separados por un espacio.")
                continue

    def productos_por_tipo(self, edad: int) -> list[Producto]:
        """
        Busca productos por tipo.

        Args:
            edad (int): Edad del cliente.

        Returns:
            list[Producto]: Lista de productos del tipo especificado.
        """
        productos_seleccionados = []
        tipos = ["Bebida alcoholic", "Bebida non-alcoholic", "Alimento", "Paquete"]
        while True:
            try:
                tipo = input(f"Ingrese el tipo de producto ({tipos}): ")
                if tipo not in tipos:
                    raise ValueError
                if edad < 18 and tipo == "Bebida alcoholic":
                    print("El cliente es menor de 18, no puede comprar bebidas alcohólicas.")
                    continue
                lp = [producto for producto in self.productos if producto.tipo == tipo]
                if len(lp) == 0:
                    raise ValueError
                productos_seleccionados.extend(seleccion_multiple(lp))
                sn = input("Desea buscar otros productos por tipo? (s/n): ")
                if sn == "s":
                    continue
                else:
                    return productos_seleccionados
            except ValueError:
                print("Tipo inválido. Debe ser Bebida alcoholic, Bebida non-alcoholic, Alimento, Paquete, cuidando las mayusculas. Ten en cuenta que algunos restaurantes no tienen un tipo de producto.")
                continue

    def producto_por_nombre(self, edad: int) -> list[Producto]:
        """
        Busca productos por nombre.

        Args:
            edad (int): Edad del cliente.

        Returns:
            list[Producto]: Lista de productos que coinciden con el nombre especificado.
        """
        productos_seleccionados = []
        while True:
            nombre = input("Ingrese el nombre del producto: ")
            try:
                productos_seleccionados.extend([producto for producto in self.productos if nombre.lower() in producto.nombre.lower()])
                sn = input("Desea buscar otros productos por nombre? (s/n): ")
                if sn == "s":
                    continue
                else:
                    if edad < 18:
                        productos_seleccionados = [producto for producto in productos_seleccionados if not producto.alcoholic]
                    return productos_seleccionados
            except ValueError:
                print("Nombre inválido. Producto no está en la lista.")
                continue

    def productos_todos(self, edad: int) -> list[Producto]:
        """
        Muestra todos los productos disponibles en el restaurante.

        Args:
            edad (int): Edad del cliente.

        Returns:
            list[Producto]: Lista de todos los productos disponibles.
        """
        for i, producto in enumerate(self.productos):
            print(f"{i + 1}. {producto}")
        seleccion_productos = seleccion_multiple(self.productos)
        if edad < 18:
            seleccion_productos = [producto for producto in seleccion_productos if not producto.alcoholic]
        return seleccion_productos

    @staticmethod
    def validar_compra(compras: list[Producto], edad: int):
        """
        Valida las compras realizadas, asegurando que no se compren productos no permitidos o sin stock.

        Args:
            compras (list[Producto]): Lista de productos a comprar.
            edad (int): Edad del cliente.

        Returns:
            list[Producto]: Lista de productos válidos para la compra.
        """
        pop_idx = []
        for i, producto in enumerate(compras):
            if edad < 18 and producto.alcoholic:
                print(f"Usted es menor de edad, por lo tanto no puede comprar {producto.nombre}")
                pop_idx.append(i)
            if producto.stock < 1:
                print(f"Producto {producto.nombre} no disponible")
                pop_idx.append(i)
        return [compras[i] for i in range(len(compras)) if i not in pop_idx]

    def iniciar_compra(self, edad: int):
        """
        Inicia el proceso de compra, permitiendo buscar productos por diferentes criterios.

        Args:
            edad (int): Edad del cliente.

        Returns:
            list[Producto]: Lista de productos seleccionados y validados para la compra.
        """
        compra = []
        while True:
            sel = input("Como quiere buscar los productos?\n\t1. Por rango de precio\n\t2. Por nombre\n\t3. Por tipo\n\t4. Mostrar todos\n\tSeleccione una opción: ")
            if sel not in ["1", "2", "3", "4"]:
                print("Opción inválida.")
                continue
            if sel == "1":
                compra.extend(self.productos_por_precio(edad))
            elif sel == "2":
                compra.extend(self.producto_por_nombre(edad))
            elif sel == "3":
                compra.extend(self.productos_por_tipo(edad))
            elif sel == "4":
                compra.extend(self.productos_todos(edad))
            else:
                print("Opción inválida.")
                continue
            sn = input("Desea buscar otros productos? (s/n): ")
            if sn == "s":
                continue
            else:
                return self.validar_compra(compra, edad)

    def __str__(self):
        """
        Retorna una representación en cadena del restaurante.

        Returns:
            str: Representación del restaurante.
        """
        return f"{self.nombre}"