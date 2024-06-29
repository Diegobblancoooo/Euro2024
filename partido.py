from funciones_ayudante import generar_id
from equipo import Equipo


class Partido:
    """
    Representa un partido de fútbol entre dos equipos.

    Attributes:
        id (str): Identificador único del partido.
        equipo_local (Equipo): El equipo que juega como local.
        equipo_visitante (Equipo): El equipo que juega como visitante.
        fecha (str): La fecha en la que se jugará el partido.
        estadio: El estadio donde se jugará el partido.
        entradas (list): Lista de entradas registradas para el partido.
        asistencia (int): Número de asistentes al partido.
        letras (list): Lista de letras utilizadas para la numeración de asientos.
        mapa_asientos_vip (dict): Mapa de asientos VIP, inicialmente vacío.
        mapa_asientos_general (dict): Mapa de asientos generales, inicialmente vacío.
    """

    def __init__(self, equipo_local: Equipo, equipo_visitante: Equipo, fecha: str, estadio):
        """
        Inicializa una instancia de la clase Partido.

        Args:
            equipo_local (Equipo): El equipo que juega como local.
            equipo_visitante (Equipo): El equipo que juega como visitante.
            fecha (str): La fecha en la que se jugará el partido.
            estadio: El estadio donde se jugará el partido.
        """
        self.id = generar_id(equipo_local.nombre, equipo_visitante.nombre, estadio.nombre)
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.fecha = fecha
        self.estadio = estadio
        self.entradas = []
        self.asistencia = 0
        self.letras = ["A", "B", "C", "D", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
        self.mapa_asientos_vip = None
        self.mapa_asientos_general = None
        self.mapa_asientos()

    def registrar_entrada(self, entrada):
        """
        Registra una entrada en la lista de entradas del partido.

        Args:
            entrada: La entrada a registrar.
        """
        self.entradas.append(entrada)

    def mapa_asientos(self):
        """
        Inicializa los mapas de asientos VIP y generales con su numeración correspondiente.
        """
        self.mapa_asientos_vip = {f"v{letra}{num}": False for letra in self.letras for num in range(1, self.estadio.asientos[0])}
        self.mapa_asientos_general = {f"{letra}{num}": False for letra in self.letras for num in range(1, self.estadio.asientos[1])}

    def modificar_asientos(self, vip: bool):
        """
        Modifica el estado de los asientos, permitiendo marcar un asiento como ocupado.

        Args:
            vip (bool): Indica si se modificará un asiento VIP o general.

        Returns:
            str: El asiento modificado.
        """
        mapa_asientos = self.mapa_asientos_vip if vip else self.mapa_asientos_general
        prefix = 'v' if vip else ''
        num_asientos = self.estadio.asientos[0] if vip else self.estadio.asientos[1]

        for num in range(1, num_asientos):
            row = [f"X" if mapa_asientos[f"{prefix}{letra}{num}"] else f"{prefix}{letra}{num}" for letra in self.letras]
            print(num, ' '.join(row), "\n")

        while True:
            try:
                asiento = input("Ingrese el asiento: ")
                if vip:
                    if not self.mapa_asientos_vip[asiento]:
                        self.mapa_asientos_vip[asiento] = True
                        return asiento
                else:
                    if not self.mapa_asientos_general[asiento]:
                        self.mapa_asientos_general[asiento] = True
                        return asiento
            except KeyError:
                pass
            print("Asiento invalido. Intente de nuevo.")

    def modificar_asientos_(self, vip: bool, asiento: str):
        """
        Modifica el estado de un asiento específico.

        Args:
            vip (bool): Indica si se modificará un asiento VIP o general.
            asiento (str): El identificador del asiento a modificar.
        """
        if vip:
            self.mapa_asientos_vip[asiento] = True
        else:
            self.mapa_asientos_general[asiento] = True

    def __str__(self):
        """
        Retorna una representación en cadena del partido.

        Returns:
            str: Representación del partido.
        """
        return f"{self.equipo_local} vs {self.equipo_visitante} en {self.estadio} el {self.fecha}"
