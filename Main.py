# 1. IMPORTAR LIBRERÍAS (Traer herramientas externas)
import math # Usaremos esta librería para redondear números

# 2. LA CLASE (El molde o diseño de nuestra herramienta)
class CalculadoraPropinas:
    def __init__(self, servicio):
        self.calidad_servicio = servicio # Guardamos qué tan bien nos atendieron

    # 3. LA FUNCIÓN (La acción específica de calcular)
    def calcular(self, monto_cuenta):
        # Usamos una lógica simple de "Si/Sino"
        if self.calidad_servicio == "excelente":
            porcentaje = 0.20 # 20%
        else:
            porcentaje = 0.10 # 10%
        
        propina = monto_cuenta * porcentaje
        return math.ceil(propina) # Redondeamos hacia arriba con la librería math
# --- 4. EL FLUJO PRINCIPAL (Donde ocurre la magia) ---

# Declaración de variables mediante interacción (Input)
total = float(input("¿Cuánto fue el total de la cuenta? "))
atencion = input("¿Cómo fue el servicio? (excelente/normal): ")

# Creamos el objeto basado en la Clase
mi_maquina = CalculadoraPropinas(atencion)

# Llamamos a la función y guardamos el resultado
resultado_final = mi_maquina.calcular(total)

# 5. SALIDA (El programa nos habla)
print(f"Deberías dejar una propina de: ${resultado_final}")

