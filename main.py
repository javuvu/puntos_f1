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
                datos = json.load(f)
                datos = json.load(f)
                self.predicciones = datos.get("predicciones", {"Javier": {}, "Lara": {}})
                self.predicciones_escuderias = datos.get("predicciones_escuderias", {"Javier": {}, "Lara": {}})
                self.resultados = datos.get("resultados", {})
                self.resultados_escuderias = datos.get("resultados_escuderias", {})
                self.puntos = datos.get("puntos", {"Javier": 0, "Lara": 0})
        except FileNotFoundError:
            pass

    # Guardar una nueva predicción
    def new_pred(self, nombre, carrera, prediccion, escuderias):
        if nombre in self.predicciones and len(prediccion) == 3 and len(escuderias) == 3:
            self.predicciones[nombre][carrera] = prediccion
            self.predicciones_escuderias[carrera] = escuderias
            self.calcular_puntos(carrera)
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
        
        for nombre in self.predicciones:
            if carrera in self.predicciones[nombre] and self.predicciones[nombre][carrera] == resultado:
                self.puntos[nombre] += 3
            
            if carrera in self.predicciones_escuderias[nombre] and self.predicciones_escuderias[nombre][carrera] == resultado_escuderias:
                self.puntos[nombre] += 2

    #Para mostrar los puntos que tenemos
    def puntos(self):
        print("Puntos actuales:")
        for nombre, puntos in self.puntos.items():
            print(f"{nombre}: {puntos} puntos")

# Definir los pilotos y las carreras
pilotos = ["Norris", "Piastri", "Verstappen", "Lawson", "Russell", "Antonelli", "Leclerc", "Hamilton", "Alonso", "Stroll", "Tsunoda", "Hadjar", "Sainz", "Albon", "Gasly", "Doohan", "Bearman", "Ocon", "Hulkenberg", "Bortoleto"]
escuderias = ["Mclaren", "Red Bull", "Mercedes", "Ferrari", "Aston Martin", "RB", "Williams", "Alpine", "Haas", "Sauber"]
carreras = 24
sistema = SistemaPuntos(pilotos, escuderias, carreras)

# Ejemplo de uso
sistema.new_pred("Javier", 1, ["Hamilton", "Verstappen", "Leclerc"], ["Mercedes", "Red Bull", "Ferrari"])
sistema.new_pred("Lara", 1, ["Sainz", "Norris", "Alonso"], ["Aston Martin", "Mclaren", "Ferrari"])

sistema.new_result(1, ["Sainz", "Norris", "Alonso"], ["Aston Martin", "Mclaren", "Ferrari"])
sistema.puntos

# --- To-do List ---
# Función para calcular el top 3 de escuderías a través de la clasificación final
# Introducir el top 3 de pilotos y escuderías utilizando "input"
# Función para mostrar la clasificación de forma bonita
# Implementar algo parecido a usar comandos (/help, /new_pred, /new_result, /clasificacion, etc)
# Función para mostrar simplemente los nombres de todos los pilotos y escuderías de forma ordenada
# Hacer un readme
# Trabajar mejor con el archivo de datos.json (¿?)
# Investigar gitignore