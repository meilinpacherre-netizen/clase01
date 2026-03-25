import pandas as pd # Herramienta para crear el Excel
from datetime import datetime # Para registrar la fecha y hora exacta

# 1. EL MOLDE: La clase que representa cada servicio
class ServicioVeterinario:
    def __init__(self, mascota, tipo):
        self.mascota = mascota
        self.tipo = tipo
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Diccionario de precios (Nuestra lista de precios)
        precios = {
            "atencion": 50,
            "baño": 60,
            "corte": 100,
            "baño/corte": 100,
            "medica": 40
        }
        # Asignamos el costo buscando en el diccionario
        self.costo = precios.get(tipo.lower(), 0)

# 2. LA BASE DE DATOS (Una lista vacía al inicio)
base_datos = []
# 3. EL BUCLE PRINCIPAL (El programa corre hasta que decidamos salir)
while True:
    print("\n--- SISTEMA DE RECEPCIÓN VET ---")
    print("1. Ingresar nueva atención")
    
    # El reporte solo aparece si hay datos
    if len(base_datos) > 0:
        print("2. Generar reporte Excel y Salir")
    
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        nombre = input("Nombre de la mascota: ")
        print("Servicios: atencion, baño, corte, baño/corte, medica")
        tipo_servicio = input("Tipo de servicio: ")
        
        # Creamos el objeto y lo guardamos en la lista
        nuevo_servicio = ServicioVeterinario(nombre, tipo_servicio)
        base_datos.append(nuevo_servicio)
        print(f"✅ ¡{nombre} ingresado con éxito!")

    elif opcion == "2" and len(base_datos) > 0:
        # Convertimos nuestra lista de objetos a una lista de diccionarios para Pandas
        datos_para_excel = []
        for s in base_datos:
            datos_para_excel.append({
                "Mascota": s.mascota,
                "Atención": s.tipo,
                "Fecha": s.fecha,
                "Costo (Soles)": s.costo
            })
        
        # Creamos el archivo Excel
        df = pd.DataFrame(datos_para_excel)
        df.to_excel("reporte_veterinaria.xlsx", index=False)
        print("📊 Reporte 'reporte_veterinaria.xlsx' generado. ¡Hasta luego!")
        break
