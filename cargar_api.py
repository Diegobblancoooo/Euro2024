import requests
from equipo import Equipo
from estadio import Estadio
from partido import Partido
from restaurantes import Restaurante
from funciones_ayudante import find_item, file_exists


class CargarApi:
    """
    Clase para cargar datos de equipos, estadios y partidos desde una API o archivos locales.

    Attributes:
        equipos (list): Lista de objetos Equipo.
        estadios (list): Lista de objetos Estadio.
        partidos (list): Lista de objetos Partido.
    """

    def __init__(self):
        """
        Inicializa una instancia de la clase CargarApi y carga los datos.
        """
        self.equipos = []
        self.estadios = []
        self.partidos = []

        self._cargar_equipos()
        self._cargar_estadios()
        self._cargar_partidos()

    def _cargar_equipos(self):
        """
        Carga los equipos desde un archivo local o desde una API si el archivo no existe.
        """
        filename = "equipos.txt"
        url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json"
        if file_exists(filename):
            self.cargar_equipos()
        else:
            self._fetch_and_save_data(url, filename)
            self.cargar_equipos()

    def _cargar_estadios(self):
        """
        Carga los estadios desde un archivo local o desde una API si el archivo no existe.
        """
        filename = "estadios.txt"
        url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json"
        if file_exists(filename):
            self.cargar_estadios()
        else:
            self._fetch_and_save_data(url, filename)
            self.cargar_estadios()

    def _cargar_partidos(self):
        """
        Carga los partidos desde un archivo local o desde una API si el archivo no existe.
        """
        filename = "partidos.txt"
        url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json"
        if file_exists(filename):
            self.cargar_partidos()
        else:
            self._fetch_and_save_data(url, filename)
            self.cargar_partidos()

    def _fetch_and_save_data(self, url, filename):
        """
        Descarga datos desde una URL y los guarda en un archivo.

        Args:
            url (str): La URL desde la cual se descargan los datos.
            filename (str): El nombre del archivo donde se guardarán los datos.
        """
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            with open(filename, "w") as file:
                file.write(str(data))
        else:
            print(f"Error fetching data from {url}")

    def cargar_equipos(self):
        """
        Carga los datos de equipos desde un archivo y crea instancias de Equipo.
        """
        with open("equipos.txt", "r") as file:
            data = eval(file.read())
            for item in data:
                equipo = Equipo(item["id"], item['name'], item['code'], item['group'])
                self.equipos.append(equipo)

    def cargar_estadios(self):
        """
        Carga los datos de estadios desde un archivo y crea instancias de Estadio.
        """
        with open("estadios.txt", "r") as file:
            data = eval(file.read())
            for item in data:
                restaurantes = [Restaurante(rest["name"], rest["products"]) for rest in item["restaurants"]]
                estadio = Estadio(item['id'], item['name'], item['city'], item['capacity'], restaurantes)
                self.estadios.append(estadio)

    def cargar_partidos(self):
        """
        Carga los datos de partidos desde un archivo y crea instancias de Partido.
        """
        with open("partidos.txt", "r") as file:
            data = eval(file.read())
            for item in data:
                equipo_local = find_item(self.equipos, lambda equipo: equipo.id == item['home']['id'])
                equipo_visitante = find_item(self.equipos, lambda equipo: equipo.id == item['away']['id'])
                estadio = find_item(self.estadios, lambda estadio: estadio.id == item['stadium_id'])

                if equipo_local is None and equipo_visitante is None or estadio is None:
                    continue
                partido = Partido(equipo_local, equipo_visitante, item['date'], estadio)
                self.partidos.append(partido)