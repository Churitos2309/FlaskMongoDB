from flask import Flask, request, redirect, url_for, render_template, session  # Importa las clases y funciones necesarias de Flask
from functools import wraps  # Importa wraps desde functools para los decoradores


# Define una lista de URLs que no requieren autenticacion
urls_sin_autentificacion = ['/login']

# Decorador para verificar la autenticacion del usuario
def verificar_autenticacion(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        # Verifica si la ruta actual requiere autenticacion y si el usuario esta autenticado
        if request.path not in urls_sin_autentificacion and 'username' not in session:
            return redirect(url_for('login'))  # Redirige a la pagina de inicio de sesion si el usuario no esta autenticado
        return func(*args, **kwargs)  # Ejecuta la función de vista
    return decorador 