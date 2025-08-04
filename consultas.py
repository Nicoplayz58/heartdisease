import psycopg2

def conectar():
    return psycopg2.connect(
        host="localhost",       # Cambia si tu DB está en otro host
        port="5432",
        dbname="heart",
        user="postgres",        # Cambia por tu usuario real
        password="ansrodriguez1"  # Cambia por tu contraseña real
    )

def obtener_total_registros():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM heart_data;")
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return total

def obtener_promedios():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            AVG(age), AVG(trestbps), AVG(chol), AVG(thalach)
        FROM heart_data;
    """)
    resultados = cur.fetchone()
    cur.close()
    conn.close()
    return {
        "edad_promedio": resultados[0],
        "presion_promedio": resultados[1],
        "colesterol_promedio": resultados[2],
        "thalach_promedio": resultados[3],
    }

if __name__ == "__main__":
    print("Total de registros:", obtener_total_registros())
    print("Promedios:", obtener_promedios())
