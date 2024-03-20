from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
from controlador.auth import verificar_autenticacion
# from controlador.userController import verificar_autenticacion






app = Flask(__name__)
app.secret_key = 'LoQueYoDesee'

from controlador.userController import *
from controlador.productsController import *


    


if __name__ == '__main__':
    app.run(debug=True, port=4000)