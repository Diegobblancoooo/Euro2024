from collections import Counter
from entrada import Entrada
from producto import Producto
from restaurantes import Restaurante
from funciones_ayudante import numero_perfecto


class Factura:
    """
    Representa una factura de compra en un restaurante.

    Attributes:
        entrada (Entrada): Entrada asociada a la factura.
        cliente (Cliente): Cliente que realizó la compra.
        productos (list[Producto]): Lista de productos comprados.
        restaurante (Restaurante): Restaurante donde se realizó la compra.
        status (bool): Indica si la factura fue generada durante el run del programa o cargada de datos guardados.
        total (float): Total a pagar de la factura.
        descuento (float): Descuento aplicado a la factura.
        subtotal (float): Subtotal antes de aplicar IVA y descuento.
        iva (float): IVA aplicado a la factura.
    """

    def __init__(self, entrada: Entrada, productos: list[Producto], restaurante: Restaurante, status: bool = False):
        """
        Inicializa una instancia de la clase Factura.

        Args:
            entrada (Entrada): Entrada asociada a la factura.
            productos (list[Producto]): Lista de productos comprados.
            restaurante (Restaurante): Restaurante donde se realizó la compra.
            status (bool): Indica si la factura fue generada durante el run del programa o cargada de datos guardados.
        """
        self.entrada = entrada
        self.cliente = entrada.cliente
        self.productos = productos
        self.restaurante = restaurante
        self.status = status
        self.total = 0
        self.descuento = 0
        self.subtotal = 0
        self.iva = 0
        self.generar_venta()

    def generar_venta(self):
        """
        Genera la venta calculando el total, el descuento, el IVA y actualizando el stock de los productos.
        """
        for producto in self.productos:
            self.total += producto.precio
        if numero_perfecto(self.entrada.cliente.cedula):
            print("Su cedula es un numero perfecto! Se le aplicara un descuento del 15%.")
            self.descuento = self.total * 0.15
        self.iva = self.total * 0.16
        self.subtotal = self.total
        self.total += self.iva
        self.total -= self.descuento
        if not self.status:
            print(self.mostrar())
            seguir = input("Desea continuar con la compra? (s/n): ")
        else:
            seguir = "s"
        if seguir.lower() == "n":
            print("Compra cancelada.")
            return
        if not self.status:
            print("Compra realizada con exito!")
        for producto in self.productos:
            producto.stock -= 1

    def mostrar(self) -> str:
        """
        Muestra los detalles de la factura.

        Returns:
            str: Cadena con los detalles de la factura.
        """
        producto_name = [producto.nombre for producto in self.productos]
        producto_name = dict(Counter(producto_name))
        string = f"""
Cliente: {self.cliente.nombre}
Restaurante: {self.restaurante.nombre}
{'\n'.join([f"{producto} x {cantidad}" for producto, cantidad in producto_name.items()])}
Subtotal: {self.subtotal}
IVA: {self.iva}
Descuento: {self.descuento}
Total: {self.total}
        """
        return string

    def __str__(self) -> str:
        """
        Retorna una representación en cadena de la factura.

        Returns:
            str: Cadena con los detalles de la factura.
        """
        return self.mostrar()

    def __dict__(self) -> dict:
        """
        Retorna un diccionario con las características de la factura.

        Returns:
            dict: Diccionario con las características de la factura.
        """
        return {"productos": [producto.__dict__() for producto in self.productos], "restaurante": self.restaurante.nombre}
    