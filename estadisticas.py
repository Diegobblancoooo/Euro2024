import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from cargar_api import CargarApi
from statistics import mean
from funciones_restaurantes import buscar_restaurante


class Estadisticas:
    """
    Clase para calcular y graficar estadísticas relacionadas con partidos, clientes y ventas de restaurantes.

    Attributes:
        api (CargarApi): Instancia de CargarApi que contiene los datos.
        gastos (list): Lista de tuplas con gastos totales y códigos de entradas VIP.
        rotacion (int): Valor de rotación para las etiquetas de los gráficos.
    """

    def __init__(self, api: CargarApi):
        """
        Inicializa una instancia de la clase Estadisticas y ejecuta los cálculos y gráficos.

        Args:
            api (CargarApi): Instancia de CargarApi que contiene los datos.
        """
        self.api = api
        self.gastos = []
        self.rotacion = 15

        print(self.gastos_vip_promedio())
        print(self.asistencia_partidos().to_string())
        self.clientes_top()
        self.platos_top()
        self.graficar_gastos_vip()
        self.graficar_asistencia_partidos()
        self.graficar_restaurantes_max_ventas()
        self.graficar_platos_max_ventas()

    def gastos_vip_promedio(self) -> float:
        """
        Calcula el gasto promedio de las entradas VIP.

        Returns:
            float: Gasto promedio de las entradas VIP.
        """
        for partido in self.api.partidos:
            for entrada in partido.entradas:
                if entrada.tipo == 'vip':
                    entrada.calcular_gastos()
                    self.gastos.append((entrada.gastos_totales, entrada.codigo))
        return mean([gasto for gasto, _ in self.gastos])

    def graficar_gastos_vip(self):
        """
        Grafica los gastos de las entradas VIP, destacando las 5 más costosas y la línea de gasto promedio.
        """
        sorted_gastos = sorted(self.gastos, reverse=True)[:5]
        y, x = zip(*sorted_gastos)
        plt.bar(x, y)
        promedio = self.gastos_vip_promedio()
        plt.axhline(y=promedio, color='r', linestyle='--', label='Promedio')
        plt.title('Gastos VIP por Entrada')
        plt.xlabel('Codigo de Entrada')
        plt.ylabel('Gastos Totales')
        plt.show()

    def asistencia_partidos(self) -> pd.DataFrame:
        """
        Crea una tabla con las estadísticas de asistencia a los partidos.

        Returns:
            pd.DataFrame: DataFrame con las estadísticas de asistencia a los partidos.
        """
        tabla = []
        for partido in self.api.partidos:
            entradas = len(partido.entradas)
            asistencias = partido.asistencia
            relacion = asistencias / entradas if entradas else 0
            tabla.append([
                partido.id,
                f"{partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre}",
                partido.estadio.nombre,
                entradas,
                asistencias,
                relacion
            ])
        df = pd.DataFrame(tabla,
                          columns=['ID', 'Partido', 'Estadio', 'Boletos Vendidos', 'Asistencia', 'Relación Asistencia/Venta'])
        df.sort_values(by='Asistencia', ascending=False, inplace=True)
        df.sort_values(by='Boletos Vendidos', ascending=False, inplace=True)
        return df

    def graficar_asistencia_partidos(self):
        """
        Grafica la asistencia de los 10 partidos con mayor asistencia.
        """
        df = self.asistencia_partidos()
        df = df.head(10)
        df.plot(x='Partido', y='Asistencia', kind='bar', title='Asistencia por Partido')
        plt.xticks(rotation=self.rotacion)
        plt.show()

    def clientes_top(self):
        """
        Imprime los 3 clientes que han comprado más entradas.
        """
        clientes = [entrada.cliente.__str__() for partido in self.api.partidos for entrada in partido.entradas]
        top_clientes = Counter(clientes).most_common(3)
        print(top_clientes)

    def platos_top(self):
        """
        Encuentra e imprime los platos más vendidos en los restaurantes y los restaurantes con más ventas.

        Returns:
            tuple: Lista de los 5 restaurantes con más ventas y lista de los 5 platos más vendidos.
        """
        plate_counts = defaultdict(int)
        restaurant_sales = defaultdict(int)

        for partido in self.api.partidos:
            for entrada in partido.entradas:
                for factura in entrada.compras:
                    for producto in factura.productos:
                        plate_counts[producto.nombre] += 1
                    restaurant_sales[factura.restaurante.nombre] += factura.total

        sorted_restaurant_sales = sorted(restaurant_sales.items(), key=lambda x: x[1], reverse=True)
        sorted_platos = sorted(plate_counts.items(), key=lambda x: x[1], reverse=True)

        for restaurant_name, _ in sorted_restaurant_sales[:5]:
            plate_counts_by_restaurant = [(plate, count) for plate, count in plate_counts.items() if
                                          plate in [producto.nombre for producto in
                                                    buscar_restaurante(self.api, restaurant_name).productos]]
            plate_counts_by_restaurant.sort(key=lambda x: x[1], reverse=True)
            print(f"Most sold plates in {restaurant_name}: {plate_counts_by_restaurant}")
        return sorted_restaurant_sales[:5], sorted_platos[:5]

    def graficar_restaurantes_max_ventas(self):
        """
        Grafica los 5 restaurantes con más ventas.
        """
        restaurantes = self.platos_top()[0]
        x, y = zip(*restaurantes)
        plt.bar(x, y)
        plt.title('Restaurantes con más ventas')
        plt.xlabel('Restaurante')
        plt.ylabel('Ventas')
        plt.xticks(rotation=self.rotacion)
        plt.show()

    def graficar_platos_max_ventas(self):
        """
        Grafica los 5 platos más vendidos.
        """
        platos = self.platos_top()[1]
        x, y = zip(*platos)
        plt.bar(x, y)
        plt.title('Platos con más ventas')
        plt.xlabel('Plato')
        plt.ylabel('Ventas')
        plt.xticks(rotation=self.rotacion)
        plt.show()