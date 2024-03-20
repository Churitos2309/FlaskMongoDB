from flask import Flask, render_template, request, jsonify, redirect, url_for
from app import app, verificar_autenticacion  # Importa la instancia de la aplicación Flask desde el archivo app.py
# from userController import verificar_autenticacion
import database as dbase  # Importa el modulo database como dbase
from product import Product  # Importa la clase Product del modulo product

# Establece la conexion a la base de datos
db = dbase.dbConnection()

# Ruta para la pagina principal
@app.route('/')
@verificar_autenticacion
def home():
    productos = db['productos']  # Obtiene la coleccion de productos
    categorias = db['categorias']  # Obtiene la coleccion de categorias
    categoriaLista = [categoria for categoria in categorias.find()]  # Obtiene todas las categorias
    productosRecibidos = productos.find()  # Obtiene todos los productos
    return render_template('tabla.html', productos=productosRecibidos, categoriaLista=categoriaLista)  # Renderiza el template 'tabla.html' con los productos y categorias

# Método POST para agregar productos

@app.route('/productos', methods=['POST'])
@verificar_autenticacion
def addProducts():
    productos = db['productos']  # Obtiene la coleccion de productos
    codigo = request.form['codigo']  # Obtiene el codigo del formulario
    nombre = request.form['nombre']  # Obtiene el nombre del formulario
    precio = request.form['precio']  # Obtiene el precio del formulario
    categoria = request.form['categoria']  # Obtiene la categoria del formulario
    
    if codigo and nombre and precio and categoria:  # Verifica si todos los campos tienen valores
        producto = Product(codigo, nombre, precio, categoria)  # Crea un objeto Product
        productos.insert_one(producto.toDBCollection())  # Inserta el producto en la base de datos
        return redirect(url_for('home'))  # Redirige a la pagina principal
    else:
        return notFound()  # Llama a la funcion notFound si faltan campos

# Metodo DELETE para eliminar productos

@app.route('/delete/<string:producto_nombre>')
@verificar_autenticacion
def delete(producto_nombre):
    productos = db['productos']  # Obtiene la coleccion de productos
    productos.delete_one({'codigo': producto_nombre})  # Elimina el producto por su codigo
    return redirect(url_for('home'))  # Redirige a la pagina principal

# Metodo PUT para modificar productos

@app.route('/edit/<string:producto_nombre>', methods=['POST'])
@verificar_autenticacion
def edit(producto_nombre):
    productos = db['productos']  # Obtiene la coleccion de productos
    codigo = request.form['codigo']  # Obtiene el codigo del formulario
    nombre = request.form['nombre']  # Obtiene el nombre del formulario
    precio = request.form['precio']  # Obtiene el precio del formulario
    categoria = request.form['categoria']  # Obtiene la categoría del formulario
    
    if codigo and nombre and precio and categoria:  # Verifica si todos los campos tienen valores
        productos.update_one({'codigo': producto_nombre}, {'$set': {'codigo': codigo, 'precio': precio, 'categoria': categoria}})  # Actualiza el producto en la base de datos
        return redirect(url_for('home'))  # Redirige a la pagina principal
    else:
        return notFound()  # Llama a la funcion notFound si faltan campos

# Manejador de errores para la pagina 404
@app.errorhandler(404)
def notFound(error=None):
    mensaje = {
        'mensaje': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    respuesta = jsonify(mensaje)  # Crea una respuesta JSON con el mensaje de error
    respuesta.status_code = 404  # Establece el código de estado 404
    return respuesta  # Retorna la respuesta JSON