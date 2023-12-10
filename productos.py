import mysql.connector


class Catalogo:
    def __init__(self, host, user, password, database):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor(dictionary=True)
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    precio FLOAT NOT NULL,
                    imagen VARCHAR(255) NOT NULL
                )
            ''')
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")

    def cerrar_conexion(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    def ejecutar_consulta(self, query, data=None):
        try:
            self.cursor.execute(query, data)
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error en la consulta SQL: {err}")
            return False

    def agregar_producto(self, codigo, descripcion, cantidad, precio, img):
        query = "INSERT INTO productos (codigo, descripcion, cantidad, precio, img) VALUES (%s, %s, %s, %s, %s);"
        data = (codigo, descripcion, cantidad, precio, img)
        
        if self.ejecutar_consulta(query, data):
            return True
        else:
            return False

    def consultar_producto(self, codigo):
        query = "SELECT * FROM productos WHERE codigo = %s;"
        data = (codigo)
        
        self.cursor.execute(query, data)
        return self.cursor.fetchone()

    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_img):
        query = "UPDATE productos SET descripcion = %s, cantidad = %s, precio = %s, proveedor = %s WHERE codigo = %s;"
        data = (nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_img, codigo)
        
        return self.ejecutar_consulta(query, data)

    def listar_productos(self):
        query = "SELECT * FROM productos;"
        self.cursor.execute(query)
        productos = self.cursor.fetchall()
        return productos

    def eliminar_producto(self, codigo):
        query = "DELETE FROM productos WHERE codigo = %s;"
        data = (codigo)
        
        return self.ejecutar_consulta(query, data)