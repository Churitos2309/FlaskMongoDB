from flask import Flask, render_template, request, jsonify, redirect, url_for
from app import app, verificar_autenticacion  # Importa la instancia de la aplicación Flask desde el archivo app.py
from bson import ObjectId
# from userController import verificar_autenticacion
import database as dbase  # Importa el modulo database como dbase
from product import Product  # Importa la clase Product del modulo product

# Establece la conexion a la base de datos
db = dbase.dbConnection()
productos = db['productos']
categorias = db['categorias']


# Ruta para la pagina principal
@app.route('/')
@verificar_autenticacion
def home():
    
    categoriaLista = [categoria for categoria in categorias.find()]  # Obtiene todas las categorias
    productosRecibidos = productos.find()  # Obtiene todos los productos
    
    por_pagina = request.args.get('pagina', 1, type=int)
    productos_por_pagina = 3
    
    total_productos = productos.count_documents({})
    print(total_productos)
    
    total_paginas = (total_productos + productos_por_pagina - 1) // productos_por_pagina 
    
    inicio_indice = (por_pagina - 1) * productos_por_pagina
    final_indice = min(inicio_indice + productos_por_pagina, total_productos)
    
    productos_paginados = productos.find().skip(inicio_indice).limit(final_indice)
    
    return render_template('tabla.html', 
                           categoriaLista=categoriaLista,
                           productos=productos_paginados, 
                           por_pagina=por_pagina, 
                           total_productos=total_productos,
                           total_paginas = total_paginas
                           )
    
    
    # productos = db['productos']  # Obtiene la coleccion de productos
    # categorias = db['categorias']  # Obtiene la coleccion de categorias
    #return render_template('tabla.html', productos=productosRecibidos, categoriaLista=categoriaLista)  # Renderiza el template 'tabla.html' con los productos y categorias

# # Método POST para agregar productos

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

@app.route('/delete/<string:producto_id>')
@verificar_autenticacion
def delete (producto_id):
    try:
        producto_id = ObjectId(producto_id)
        resultado = productos.delete_one({'_id':producto_id})
        if resultado.deleted_count == 1:
            return redirect(url_for('home'))
        else:
            return "El producto no existe o no se pudo eliminar."
    except Exception as e:
        return str(e)
    
        


# def delete(producto_id):
#     productos = db['productos']  # Obtiene la coleccion de productos
#     productos.delete_one({'id': ObjectId(producto_id)})  # Elimina el producto por su codigo
#     return redirect(url_for('home'))  # Redirige a la pagina principal

# Metodo PUT para modificar productos

@app.route('/edit/<string:producto_id>', methods=['GET','POST'])
@verificar_autenticacion
def edit(producto_id):
    if request.method == 'GET':
        producto_id = ObjectId(producto_id)
        producto = productos.find_one({'_id': producto_id})
        categorias_lista = categorias.find()
        return render_template('home.html', producto=producto, categorias_lista = categorias_lista)
    elif request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']
        
        productos.update_one({'_id': producto_id}, {'$set': {'codigo': codigo, 'nombre': nombre, 'precio': precio, 'categoria': categoria}})
        print ('Subio a la base de datos')
        
        return redirect(url_for('home'))
    
    
    
    
    
    
    
    # producto_id = ObjectId(producto_id)
    # print (producto_id)
    # # productos = db['productos']  # Obtiene la coleccion de productos
    # codigo = request.form['codigo']  # Obtiene el codigo del formulario
    # nombre = request.form['nombre']  # Obtiene el nombre del formulario
    # precio = request.form['precio']  # Obtiene el precio del formulario
    # categoria = request.form['categoria']  # Obtiene la categoría del formulario
    
    # if codigo and nombre and precio and categoria:  # Verifica si todos los campos tienen valores
    #     productos.update_one({'_id': producto_id}, {'$set': {'codigo': codigo,'nombre': nombre, 'precio': precio, 'categoria': categoria}})  # Actualiza el producto en la base de datos
    #     return redirect(url_for('home'))  # Redirige a la pagina principal
    # else:
    #     return notFound()  # Llama a la funcion notFound si faltan campos
    

    



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