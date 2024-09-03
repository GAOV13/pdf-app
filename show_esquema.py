import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('./instance/site.db')

# Crear un cursor
cursor = conn.cursor()

# Ejecutar una consulta para obtener el esquema de la base de datos
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")

# Obtener todos los resultados
tables = cursor.fetchall()

# Imprimir el esquema de cada tabla
for table in tables:
    print(table[0])

# Cerrar la conexión

conn.close()