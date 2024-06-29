class Estadio:
    """
    Representa un estadio de fútbol.

    Attributes:
        id (str): Identificador único del estadio.
        nombre (str): Nombre del estadio.
        ubicacion (str): Ubicación del estadio.
        asientos (list[int]): Lista con el número de asientos disponibles en diferentes secciones.
        restaurantes (list): Lista de restaurantes disponibles en el estadio.
    """

    def __init__(self, e_id: str, nombre: str, ubicacion: str, asientos: list[int], restaurantes: list):
        """
        Inicializa una instancia de la clase Estadio.

        Args:
            e_id (str): Identificador único del estadio.
            nombre (str): Nombre del estadio.
            ubicacion (str): Ubicación del estadio.
            asientos (list[int]): Lista con el número de asientos disponibles en diferentes secciones.
            restaurantes (list): Lista de restaurantes disponibles en el estadio.
        """
        self.id = e_id
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.asientos = asientos
        self.restaurantes = restaurantes

    def __str__(self):
        """
        Retorna una representación en cadena del estadio.

        Returns:
            str: Nombre del estadio.
        """
        return self.nombre