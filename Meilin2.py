from datetime import datetime
from openpyxl import Workbook

# =========================
# BASE DE DATOS
# =========================
servicios = []

# =========================
# PRECIOS
# =========================
PRECIOS = {
    "baño": 50,
    "corte": 60,
    "baño/corte": 100,
    "atención médica": 40
}

TIPOS_MASCOTA = {
    1: "Perro",
    2: "Gato",
    3: "Conejo",
    4: "Hámster",
    5: "Loro"
}

EXTRAS_MEDICOS = {
    1: ("consulta simple", 0),
    2: ("vacunas", 30),
    3: ("profilaxis", 150),
    4: ("cirugías", 1000)
}

MEDICOS = ["Meilin", "Renzo", "Maya"]

METODOS_PAGO = {
    1: "Efectivo",
    2: "Tarjeta"
}

TIPOS_COMPROBANTE = {
    1: "Boleta",
    2: "Factura"
}

# =========================
# CLASE
# =========================
class Servicio:
    def __init__(self, mascota, tipo_mascota, duenio, tipo, costo,
                 medico="-", metodo_pago="", comprobante="", ruc="-"):
        
        self.mascota = mascota
        self.tipo_mascota = tipo_mascota
        self.duenio = duenio
        self.tipo = tipo
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.costo = costo
        self.medico = medico
        self.metodo_pago = metodo_pago
        self.comprobante = comprobante
        self.ruc = ruc

# =========================
# INGRESO DE ATENCIÓN
# =========================
def ingresar_atencion():
    print("\n--- INGRESO DE ATENCIÓN ---")

    mascota = input("Nombre de la mascota: ").strip()
    duenio = input("Nombre del dueño: ").strip()

    # Tipo de mascota
    print("\nTipo de mascota:")
    for k, v in TIPOS_MASCOTA.items():
        print(f"{k}. {v}")

    try:
        tipo_mascota = TIPOS_MASCOTA[int(input("Seleccione tipo: "))]
    except:
        print("❌ Tipo inválido")
        return

    # Servicios
    print("\nServicios:")
    tipos = list(PRECIOS.keys())
    for i, t in enumerate(tipos, 1):
        print(f"{i}. {t} - S/ {PRECIOS[t]}")

    try:
        tipo = tipos[int(input("Seleccione servicio: ")) - 1]
    except:
        print("❌ Opción inválida")
        return

    costo = PRECIOS[tipo]
    medico = "-"

    # =========================
    # ATENCIÓN MÉDICA
    # =========================
    if tipo == "atención médica":

        print("\nTipo de atención médica:")
        for k, v in EXTRAS_MEDICOS.items():
            print(f"{k}. {v[0]} (+S/ {v[1]})")

        try:
            op_extra = int(input("Seleccione opción: "))
            nombre_extra, precio_extra = EXTRAS_MEDICOS[op_extra]
        except:
            print("❌ Opción inválida")
            return

        costo += precio_extra
        tipo = f"Atención médica - {nombre_extra}"

        # Médico
        print("\nMédicos disponibles:")
        for i, m in enumerate(MEDICOS, 1):
            print(f"{i}. {m}")

        try:
            medico = MEDICOS[int(input("Seleccione médico: ")) - 1]
        except:
            print("❌ Médico inválido")
            return

    # =========================
    # MÉTODO DE PAGO
    # =========================
    print("\nMétodo de pago:")
    for k, v in METODOS_PAGO.items():
        print(f"{k}. {v}")

    try:
        metodo_pago = METODOS_PAGO[int(input("Seleccione método: "))]
    except:
        print("❌ Método inválido")
        return

    # =========================
    # COMPROBANTE
    # =========================
    print("\nTipo de comprobante:")
    for k, v in TIPOS_COMPROBANTE.items():
        print(f"{k}. {v}")

    try:
        comprobante = TIPOS_COMPROBANTE[int(input("Seleccione: "))]
    except:
        print("❌ Opción inválida")
        return

    ruc = "-"

    if comprobante == "Factura":
        ruc = input("Ingrese N° de RUC: ").strip()

        if len(ruc) != 11 or not ruc.isdigit():
            print("❌ RUC inválido (debe tener 11 dígitos)")
            return

    # =========================
    # GUARDAR
    # =========================
    servicio = Servicio(
        mascota,
        tipo_mascota,
        duenio,
        tipo,
        costo,
        medico,
        metodo_pago,
        comprobante,
        ruc
    )

    servicios.append(servicio)

    print("✅ Atención registrada correctamente")

# =========================
# REPORTE
# =========================
def generar_reporte():
    print("\n--- GENERANDO REPORTE ---")

    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte Veterinaria"

    ws.append([
        "Mascota",
        "Tipo Mascota",
        "Dueño",
        "Atención",
        "Fecha",
        "Costo",
        "Médico",
        "Método Pago",
        "Comprobante",
        "RUC"
    ])

    for s in servicios:
        ws.append([
            s.mascota,
            s.tipo_mascota,
            s.duenio,
            s.tipo,
            s.fecha,
            s.costo,
            s.medico,
            s.metodo_pago,
            s.comprobante,
            s.ruc
        ])

    wb.save("reporte_veterinaria.xlsx")

    print("📊 Reporte generado correctamente")

# =========================
# MENÚ
# =========================
def menu():
    while True:
        print("\n=== SISTEMA VETERINARIA ===")
        print("1. Ingresar atención")

        if len(servicios) > 0:
            print("2. Mostrar reporte")

        print("0. Salir")

        opcion = input("Seleccione: ")

        if opcion == "1":
            ingresar_atencion()
        elif opcion == "2" and len(servicios) > 0:
            generar_reporte()
        elif opcion == "0":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción inválida")

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    menu()