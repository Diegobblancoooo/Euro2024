class Cliente:
    """
    Representa un cliente con sus datos personales y sus actividades de compra.

    Attributes:
        nombre (str): Nombre del cliente.
        cedula (int): Cédula de identidad del cliente.
        edad (int): Edad del cliente.
        entradas (list): Lista de entradas compradas por el cliente.
        compras (list): Lista de productos comprados por el cliente.
        gastos_totales (float): Suma total de los gastos del cliente.
    """

    def __init__(self, nombre: str, cedula: int, edad: int):
        """
        Inicializa una instancia de la clase Cliente.

        Args:
            nombre (str): Nombre del cliente.
            cedula (int): Cédula de identidad del cliente.
            edad (int): Edad del cliente.
        """
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad
        self.entradas = []
        self.compras = []
        self.gastos_totales = 0

    def calcular_gastos(self):
        """
        Calcula el total de los gastos del cliente, sumando el costo de las entradas y las compras.
        """
        gastos_entradas = sum(entrada.factura["total"] for entrada in self.entradas)
        self.gastos_totales = sum(producto.precio for producto in self.compras) + gastos_entradas

    def __str__(self):
        """
        Retorna una representación en cadena del cliente.

        Returns:
            str: Representación del cliente.
        """
        return f"{self.nombre} - {self.cedula}"

    def __eq__(self, other):
        """
        Compara si dos clientes son iguales basándose en su cédula.

        Args:
            other (Cliente): Otro cliente a comparar.

        Returns:
            bool: True si los clientes son iguales, False en caso contrario.
        """
        return self.cedula == other.cedula

    def __ne__(self, other):
        """
        Compara si dos clientes son diferentes basándose en su cédula.

        Args:
            other (Cliente): Otro cliente a comparar.

        Returns:
            bool: True si los clientes son diferentes, False en caso contrario.
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        Retorna el valor hash del cliente basado en su cédula.

        Returns:
            int: Valor hash del cliente.
        """
        return hash(self.cedula)

    def __dict__(self):
        """
        Retorna un diccionario con las características del cliente.

        Returns:
            dict: Diccionario con las características del cliente.
        """
        return {
            "nombre": self.nombre,
            "cedula": self.cedula,
            "edad": self.edad,
            "entradas": [entrada.__dict__() for entrada in self.entradas],
            "compras": [compra.__dict__() for compra in self.compras],
            "gastos_totales": self.gastos_totales
        }