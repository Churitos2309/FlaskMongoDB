class Product:
    def __init__(self, codigo, nombre, precio, categoria):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        
    def toDBCollection(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
        }