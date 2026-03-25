import mysql.connector

# --- CONFIGURACIÓN DE LA "API" ---

def conectar():
    """Establece la conexión central con XAMPP"""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="recomendacion"
        )
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None


def registrar_libro(nombre, genero, autor, anio):
    """Inserta un nuevo libro en la base de datos"""
    db = conectar()
    if db:
        cursor = db.cursor()
        query = "INSERT INTO libros (nombre, genero, autor, año) VALUES (%s, %s, %s, %s)"
        valores = (nombre, genero, autor, anio)
        cursor.execute(query, valores)
        db.commit()
        print(f"✅ Libro '{nombre}' registrado con éxito.")
        db.close()


def obtener_genero_favorito(id_usuario):
    """Calcula el género favorito basado en el promedio de puntuaciones (70% )"""
    db = conectar()
    if db:
        cursor = db.cursor()
        query = """
                SELECT l.genero, AVG(p.calificacion) as promedio
                FROM puntuacion p
                         JOIN libros l ON p.id_libro = l.id_libro
                WHERE p.id_usuario = %s
                GROUP BY l.genero
                ORDER BY promedio DESC LIMIT 1 \
                """
        cursor.execute(query, (id_usuario,))
        resultado = cursor.fetchone()
        db.close()
        return resultado[0] if resultado else None
    return None


# --- BLOQUE DE PRUEBAS (MAIN) ---

if __name__ == "__main__":
    print("--- 📚 SISTEMA DE GESTIÓN DE LIBROS ---")

    opcion = input("¿Quieres (1) Registrar un libro o (2) Ver tu género favorito? ")

    if opcion == "1":
        print("\n--- Registro de Nuevo Libro ---")
        titulo = input("Nombre del libro: ")
        gen = input("Género: ")
        aut = input("Autor: ")
        anio_pub = input("Año: ")

        registrar_libro(titulo, gen, aut, anio_pub)

    elif opcion == "2":
        # usamos el 1 por que es el id del primer usuario, lo modificare mas adelante pero por ahora lo dejare asi para las pruebas
        favorito = obtener_genero_favorito(1)
        if favorito:
            print(f"\n⭐ Basado en tus votos, tu género favorito es: {favorito}")
        else:
            print("\n⚠️ Aún no tienes suficientes votos.")
    else:
        print("Opción no válida.")