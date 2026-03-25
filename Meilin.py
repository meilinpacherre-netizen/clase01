import sqlite3
from datetime import datetime
from openpyxl import Workbook

# =========================
# CONFIGURACIÓN
# =========================

DB_NAME = "veterinaria.db"

PRECIOS = {
    "baño": 50,
    "corte": 60,
    "baño/corte": 100,
    "atención médica": 40
}

# =========================
# BASE DE DATOS
# =========================

def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mascotas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cliente_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS atenciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mascota_id INTEGER,
        tipo TEXT,
        fecha TEXT,
        costo INTEGER
    )
    """)

    conn.commit()
    conn.close()

# =========================
# CLIENTES
# =========================

def crear_cliente():
    nombre = input("Nombre del cliente: ").strip()

    if not nombre:
        print("❌ Nombre inválido")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nombre) VALUES (?)", (nombre,))
    conn.commit()
    conn.close()

    print("✅ Cliente registrado")


def obtener_clientes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    data = cursor.fetchall()
    conn.close()
    return data

# =========================
# MASCOTAS
# =========================

def crear_mascota():
    clientes = obtener_clientes()

    if not clientes:
        print("❌ Primero registra un cliente")
        return

    print("\nClientes:")
    for c in clientes:
        print(f"{c[0]}. {c[1]}")

    nombre = input("Nombre de la mascota: ").strip()
    cliente_id = int(input("ID del cliente: "))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO mascotas (nombre, cliente_id) VALUES (?, ?)",
        (nombre, cliente_id)
    )
    conn.commit()
    conn.close()

    print("✅ Mascota registrada")


def obtener_mascotas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT mascotas.id, mascotas.nombre, clientes.nombre
    FROM mascotas
    JOIN clientes ON mascotas.cliente_id = clientes.id
    """)
    data = cursor.fetchall()
    conn.close()
    return data

# =========================
# ATENCIONES
# =========================

def registrar_atencion():
    mascotas = obtener_mascotas()

    if not mascotas:
        print("❌ No hay mascotas registradas")
        return

    print("\nMascotas:")
    for m in mascotas:
        print(f"{m[0]}. {m[1]} (Dueño: {m[2]})")

    mascota_id = int(input("ID mascota: "))

    print("\nServicios:")
    tipos = list(PRECIOS.keys())
    for i, t in enumerate(tipos, 1):
        print(f"{i}. {t} - S/ {PRECIOS[t]}")

    opcion = int(input("Seleccione servicio: "))

    if 1 <= opcion <= len(tipos):
        tipo = tipos[opcion - 1]
        costo = PRECIOS[tipo]
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO atenciones (mascota_id, tipo, fecha, costo)
        VALUES (?, ?, ?, ?)
        """, (mascota_id, tipo, fecha, costo))

        conn.commit()
        conn.close()

        print("✅ Atención registrada")
    else:
        print("❌ Opción inválida")

# =========================
# REPORTES
# =========================

def ver_historial():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT mascotas.nombre, clientes.nombre, atenciones.tipo, atenciones.fecha, atenciones.costo
    FROM atenciones
    JOIN mascotas ON atenciones.mascota_id = mascotas.id
    JOIN clientes ON mascotas.cliente_id = clientes.id
    ORDER BY atenciones.fecha DESC
    """)

    datos = cursor.fetchall()
    conn.close()

    if not datos:
        print("❌ No hay registros")
        return

    print("\n=== HISTORIAL ===")
    for d in datos:
        print(f"Mascota: {d[0]} | Dueño: {d[1]} | {d[2]} | {d[3]} | S/ {d[4]}")


def generar_reporte_excel():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT mascotas.nombre, atenciones.tipo, atenciones.fecha, atenciones.costo
    FROM atenciones
    JOIN mascotas ON atenciones.mascota_id = mascotas.id
    """)

    datos = cursor.fetchall()
    conn.close()

    if not datos:
        print("❌ No hay datos para reporte")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte"

    ws.append(["Mascota", "Atención", "Fecha", "Costo"])

    for d in datos:
        ws.append(d)

    wb.save("reporte_veterinaria.xlsx")

    print("📊 Reporte generado correctamente")


def ver_ingresos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(costo) FROM atenciones")
    total = cursor.fetchone()[0]

    conn.close()

    print(f"\n💰 Total ingresos: S/ {total if total else 0}")

# =========================
# MENÚ
# =========================

def menu():
    while True:
        print("\n=== VETERINARIA ===")
        print("1. Registrar cliente")
        print("2. Registrar mascota")
        print("3. Registrar atención")
        print("4. Ver historial")
        print("5. Generar reporte Excel")
        print("6. Ver ingresos")
        print("0. Salir")

        opcion = input("Seleccione: ")

        if opcion == "1":
            crear_cliente()
        elif opcion == "2":
            crear_mascota()
        elif opcion == "3":
            registrar_atencion()
        elif opcion == "4":
            ver_historial()
        elif opcion == "5":
            generar_reporte_excel()
        elif opcion == "6":
            ver_ingresos()
        elif opcion == "0":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción inválida")

# =========================
# EJECUCIÓN
# =========================

if __name__ == "__main__":
    init_db()
    menu()