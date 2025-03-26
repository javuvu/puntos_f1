import json

class SistemaPuntos:
    def __init__(self, pilotos, escuderias, carreras, archivo="datos.json"):
        self.pilotos = pilotos
        self.escuderias = escuderias
        self.carreras = carreras
        self.archivo = archivo
        self.predicciones = {"Javier": {}, "Lara": {}}
        self.predicciones_escuderias = {"Javier": {}, "Lara": {}}
        self.resultados = {}
        self.resultados_escuderias = {}
        self.puntos_carrera = {}    # Para los puntos conseguidos en cada carrera
        self.puntos = {"Javier": 0, "Lara": 0}
        self.cargar_datos()

    # Guardamos los datos en un archivo para no perder la información
    def guardar_datos(self):
        datos = {
            "predicciones": self.predicciones,
            "predicciones_escuderias": self.predicciones_escuderias,
            "resultados": self.resultados,
            "resultados_escuderias": self.resultados_escuderias,
            "puntos": self.puntos
        }
        with open(self.archivo, "w") as f:
            json.dump(datos, f)

    def cargar_datos(self):
        try:
            with open(self.archivo, "r") as f:
                contenido = f.read().strip()
                if not contenido:  # Si el archivo está vacío, evita el error
                    return
                datos = json.loads(contenido)
                self.predicciones = datos.get("predicciones", {"Javier": {}, "Lara": {}})
                self.predicciones_escuderias = datos.get("predicciones_escuderias", {"Javier": {}, "Lara": {}})
                self.resultados = datos.get("resultados", {})
                self.resultados_escuderias = datos.get("resultados_escuderias", {})
                self.puntos = datos.get("puntos", {"Javier": 0, "Lara": 0})
        except (FileNotFoundError, json.JSONDecodeError):
            print("El archivo está corrupto o no existe o hay algún error.")
            pass  # Si el archivo no existe o está corrupto, se inicializa con valores por defecto

    """
    def cargar_datos(self):
        try:
            with open(self.archivo, "r") as f:
                datos = json.load(f)
                datos = json.load(f)
                self.predicciones = datos.get("predicciones", {"Javier": {}, "Lara": {}})
                self.predicciones_escuderias = datos.get("predicciones_escuderias", {"Javier": {}, "Lara": {}})
                self.resultados = datos.get("resultados", {})
                self.resultados_escuderias = datos.get("resultados_escuderias", {})
                self.puntos = datos.get("puntos", {"Javier": 0, "Lara": 0})
        except FileNotFoundError:
            pass"
    """

    # Guardar una nueva predicción
    def new_pred(self, nombre, carrera, prediccion, escuderias):
        if nombre in self.predicciones and len(prediccion) == 3 and len(escuderias) == 3:
            self.predicciones[nombre][carrera] = prediccion
            self.predicciones_escuderias[nombre][carrera] = escuderias
            # self.calcular_puntos(carrera)
            self.guardar_datos()
            print("Predicción hecha")
        else:
            print("Has puesto algo mal. Revisa tu predicción e inténtalo de nuevo.")

    # Guardar nuevo resultado
    def new_result(self, carrera, resultado, escuderias):
        if len(resultado) == 3 and len(escuderias) == 3:
            self.resultados[carrera] = resultado
            self.resultados_escuderias[carrera] = escuderias
            self.calcular_puntos(carrera)
            self.guardar_datos()
        else:
            print("Resultado inválido. Revisa lo que has escrito e inténtalo de nuevo")

    # Cálculo de los puntos comparando las predicciones con el resultado introducido
    def calcular_puntos(self, carrera):
        if carrera not in self.resultados or carrera not in self.resultados_escuderias:
            print(f"No hay resultado registrado para la carrera {carrera}.")
            return
        
        resultado = self.resultados[carrera]
        resultado_escuderias = self.resultados_escuderias[carrera]
        
        puntos_carrera_actual = {"Javier": 0, "Lara": 0}

        for nombre in self.predicciones:
            if carrera in self.predicciones[nombre] and self.predicciones[nombre][carrera] == resultado:
                self.puntos[nombre] += 3
                puntos_carrera_actual[nombre] += 3
            
            if carrera in self.predicciones_escuderias[nombre] and self.predicciones_escuderias[nombre][carrera] == resultado_escuderias:
                self.puntos[nombre] += 2
                puntos_carrera_actual[nombre] += 2
        
        self.puntos_carrera[carrera] = puntos_carrera_actual

    #Para mostrar los puntos que tenemos en total
    def points(self, nombre=None):
        if nombre:
            if nombre in self.puntos:
                print("Puntos actuales de", end=" ")
                print(f"{nombre}: {self.puntos[nombre]}")
            else:
                print("Te has equivocado escribiendo el nombre")
        else:
            print("Puntos actuales de", end=" ")
            print(f"Lara: {self.puntos['Lara']}")
            print("Puntos actuales de", end=" ")
            print(f"Javier: {self.puntos['Javier']}")

    #Para mostrar los puntos que hemos conseguido en una carrera en concreto
    def points_carrera(self, carrera, nombre=None):
        if carrera in self.carreras:
            print(f"Puntos de la carrera {carrera}: {self.puntos_carrera[carrera]}")
        else:
            print("Has introducido el número de la carrera mal")

    # Función para resetear a cero los puntos
    def reset_points(self):
        pass #hacer en algún momento
        

# Definir los pilotos y las carreras
pilotos = ["Norris", "Piastri", "Verstappen", "Lawson", "Russell", "Antonelli", "Leclerc", "Hamilton", "Alonso", "Stroll", "Tsunoda", "Hadjar", "Sainz", "Albon", "Gasly", "Doohan", "Bearman", "Ocon", "Hulkenberg", "Bortoleto"]
escuderias = ["Mclaren", "Red Bull", "Mercedes", "Ferrari", "Aston Martin", "RB", "Williams", "Alpine", "Haas", "Sauber"]
carreras = ["Melbourne", "Shangai", "Suzuka", "Sakhir", "Jeddah", "Miami", "Imola", "Monaco", "Barcelona", "Montreal", "Spielberg", "Silverstone", "Spa", "Budapest", "Zandvoort", "Monza", "Baku", "Singapore", "Austin", "Mexico City", "Sao Paulo", "Las Vegas", "Lusail", "Yas Marina"]
# carreras = list(range(1, 25))  # Genera una lista de números del 1 al 24
sistema = SistemaPuntos(pilotos, escuderias, carreras)

# Función simple para mostrar los pilotos
def list_pilotos():
    print("\n -- Escuderías y pilotos --")
    print("Mclaren:\tNorris - Piastri")
    print("Red Bull:\tVerstappen - Lawson")
    print("Mercedes:\tRussell - Antonelli")
    print("Ferrari:\tLeclerc - Hamilton")
    print("Aston Martin:\tAlonso - Stroll")
    print("RB:\t\tTsunoda - Hadjar")
    print("Williams:\tSainz - Albon")
    print("Alpine:\t\tGasly - Doohan")
    print("Haas:\t\tBearman - Ocon")
    print("Sauber:\t\tHulkenberg - Bortoleto\n")

# ----- Ejemplo de uso -----

# sistema.points("Javier")
# sistema.points("Lara")

sistema.new_pred("Javier", "Melbourne", ["Sainz", "Norris", "Alonso"], ["Aston Martin", "Mclaren", "Sauber"])
sistema.new_pred("Lara", "Melbourne", ["Sainz", "Norris", "Alonso"], ["Aston Martin", "Mclaren", "Ferrari"])

sistema.new_result("Melbourne", ["Sainz", "Norris", "Alonso"], ["Aston Martin", "Mclaren", "Ferrari"])
sistema.points() # Para mostrar los puntos de los dos
sistema.points_carrera("Melbourne")

list_pilotos()




# --- To-do List ---
# Función para calcular el top 3 de escuderías a través de la clasificación final
# Introducir el top 3 de pilotos y escuderías utilizando "input"
# Función para mostrar la clasificación de forma bonita
# Implementar algo parecido a usar comandos (/help, /new_pred, /new_result, /clasificacion, etc)
# Hacer un readme
# Trabajar mejor con el archivo de datos.json (¿?)