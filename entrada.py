from partido import Partido
from cliente import Cliente
from funciones_ayudante import es_numero_vampiro


class Entrada:
    """
    Representa una entrada para un partido.

    Attributes:
        tipo (str): Tipo de entrada (general o VIP).
        partido (Partido): Partido asociado a la entrada.
        asiento (str): Asiento asignado para la entrada.
        cliente (Cliente): Cliente que compró la entrada.
        codigo (str): Código de la entrada.
        validado (bool): Indica si la entrada ha sido validada.
        status (bool): Indica si la entrada fue generada durante el run del programa o cargada de datos guardados.
        precio (float): Precio de la entrada.
        factura (dict): Detalles de la factura de la entrada.
        compras (list): Lista de compras asociadas a la entrada.
        gastos_totales (float): Suma total de los gastos asociados a la entrada.
    """

    def __init__(self, tipo: str, partido: Partido, asiento: str, cliente: Cliente, codigo: str, status: bool = False):
        """
        Inicializa una instancia de la clase Entrada.

        Args:
            tipo (str): Tipo de entrada (general o VIP).
            partido (Partido): Partido asociado a la entrada.
            asiento (str): Asiento asignado para la entrada.
            cliente (Cliente): Cliente que compró la entrada.
            codigo (str): Código de la entrada.
            status (bool): Indica si la entrada fue generada durante el run del programa o cargada de datos guardados.
        """
        self.tipo = tipo
        self.partido = partido
        self.asiento = asiento
        self.cliente = cliente
        self.codigo = codigo
        self.validado = False
        self.status = status
        self.precio = 35 if tipo == 'general' else 75
        self.factura = {}
        self.calcular_precio_final()
        self.compras = []
        self.gastos_totales = 0

    def calcular_gastos(self):
        """
        Calcula el total de los gastos del cliente, sumando el costo de las compras y la entrada.
        """
        self.gastos_totales = sum(factura.total for factura in self.compras) + self.factura["total"]

    def calcular_precio_final(self):
        """
        Calcula el precio final de la entrada, aplicando descuentos si corresponde, y añade IVA.
        """
        descuento = 0
        if es_numero_vampiro(self.cliente.cedula):
            print("Su cedula es un numero vampiro! Es elegido para un 50% de descuento sobre el precio de su entrada. ")
            descuento = self.precio * 0.50
        subtotal = self.precio - descuento
        iva = subtotal * 0.16
        total = subtotal + iva
        self.precio = total
        self.factura = {"subtotal": subtotal, "descuento": descuento, "IVA": iva, "total": total}
        if not self.status:
            print(self.factura)

    def __str__(self):
        """
        Retorna una representación en cadena de la entrada.

        Returns:
            str: Representación de la entrada.
        """
        return f"Entrada para {self.partido} en el asiento {self.asiento} cedula del cliente {self.cliente.cedula}."

    def __dict__(self):
        """
        Retorna un diccionario con las características de la entrada.

        Returns:
            dict: Diccionario con las características de la entrada.
        """
        return {
            "tipo": self.tipo,
            "partido": self.partido.id,
            "asiento": self.asiento,
            "codigo": self.codigo,
            "validado": self.validado,
            "compras": [compra.__dict__() for compra in self.compras]
        }
    