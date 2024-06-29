class Equipo:
    """
    Representa un equipo de fútbol.

    Attributes:
        id (int): Identificador único del equipo.
        nombre (str): Nombre del equipo.
        codigo_fifa (str): Código FIFA del equipo.
        grupo (str): Grupo al que pertenece el equipo.
    """

    def __init__(self, id, nombre, codigo_fifa, grupo):
        """
        Inicializa una instancia de la clase Equipo.

        Args:
            id (int): Identificador único del equipo.
            nombre (str): Nombre del equipo.
            codigo_fifa (str): Código FIFA del equipo.
            grupo (str): Grupo al que pertenece el equipo.
        """
        self.id = id
        self.nombre = nombre
        self.codigo_fifa = codigo_fifa
        self.grupo = grupo

    def __str__(self):
        """
        Retorna una representación en cadena del equipo.

        Returns:
            str: Nombre del equipo.
        """
        return self.nombre