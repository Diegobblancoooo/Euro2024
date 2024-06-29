class Producto:
    """
    Representa un producto con sus características básicas.

    Attributes:
        nombre (str): Nombre del producto.
        cantidad (str): Cantidad del producto.
        precio (float): Precio del producto.
        stock (int): Cantidad de productos disponibles en stock.
        adicional (str): Información adicional sobre el producto.
        alcoholic (bool): Indica si el producto es alcohólico o no.
        tipo (str): Tipo del producto determinado por la información adicional.
    """

    def __init__(self, name: str, cantidad: str, precio: float, stock: int, adicional: str):
        """
        Inicializa una instancia de la clase Producto.

        Args:
            name (str): Nombre del producto.
            cantidad (str): Cantidad del producto.
            precio (float): Precio del producto.
            stock (int): Cantidad de productos disponibles en stock.
            adicional (str): Información adicional sobre el producto.
        """
        self.nombre = name
        self.cantidad = cantidad
        self.precio = precio
        self.stock = stock
        self.adicional = adicional
        self.alcoholic = False
        self.tipo = self.tipo_producto(adicional)

    def tipo_producto(self, adicional: str):
        """
        Determina el tipo del producto basado en la información adicional.

        Args:
            adicional (str): Información adicional sobre el producto.

        Returns:
            str: Tipo del producto.
        """
        if adicional == "non-alcoholic" or adicional == "alcoholic":
            if adicional == "alcoholic":
                self.alcoholic = True
            return f"Bebida {adicional}"
        elif adicional == "plate":
            return "Alimento"
        else:
            return "Paquete"
        
    def __str__(self):
        """
        Retorna una representación en cadena del producto.

        Returns:
            str: Representación del producto.
        """
        return f"{self.nombre}, tipo: {self.tipo}, precio: {self.precio}, stock: {self.stock}"

    def __eq__(self, other):
        """
        Compara si dos productos son iguales basándose en su nombre.

        Args:
            other (Producto): Otro producto a comparar.

        Returns:
            bool: True si los productos son iguales, False en caso contrario.
        """
        return self.nombre == other.nombre

    def __ne__(self, other):
        """
        Compara si dos productos son diferentes basándose en su nombre.

        Args:
            other (Producto): Otro producto a comparar.

        Returns:
            bool: True si los productos son diferentes, False en caso contrario.
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        Retorna el valor hash del producto basado en su nombre.

        Returns:
            int: Valor hash del producto.
        """
        return hash(self.nombre)

    def __dict__(self):
        """
        Retorna un diccionario con las características del producto.

        Returns:
            dict: Diccionario con las características del producto.
        """
        return {"nombre": self.nombre, "cantidad": self.cantidad, "precio": self.precio, "stock": self.stock, "tipo": self.tipo, "adicional": self.adicional}