from flask import render_template, url_for, flash, redirect, request, current_app, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import Usuario, Resultado
from app.forms import RegistrationForm, LoginForm, UpdateProfileForm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from typing import Dict, List
import json
import uuid
from collections import Counter
from sqlalchemy import inspect
from sqlalchemy.exc import DatabaseError
import os
import time

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/home')
def home():
    return render_template('home.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Redirigir a la página principal si el usuario ya está autenticado
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    
    # Validar el formulario al enviarlo
    if form.validate_on_submit():
        # Verificar si el nombre de usuario o el correo electrónico ya existen en la base de datos
        existing_user = Usuario.query.filter(
            (Usuario.username == form.username.data) | (Usuario.email == form.email.data)
        ).first()
        
        if existing_user:
            # Mostrar un mensaje de error si el usuario ya existe
            flash('El nombre de usuario o el correo electrónico ya están en uso. Por favor, elige otros.', 'danger')
        else:
            # Crear un nuevo usuario si no existe
            user = Usuario(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Tu cuenta ha sido creada exitosamente!', 'success')
            return redirect(url_for('main.login'))
    
    # Renderizar la plantilla de registro con el formulario
    return render_template('register.html', title='Registro', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.menu'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.menu'))
        else:
            flash('Login fallido. Por favor, verifica tu email y contraseña', 'danger')
    return render_template('login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@bp.route('/menu')
@login_required
def menu():
    return render_template('menu.html', title='Menu')

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash('Tu perfil ha sido actualizado!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    return render_template('profile.html', title='Perfil', form=form)

@bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    """Permite al usuario eliminar su cuenta marcándola como inactiva."""
    current_user.activo = False  # Marcar al usuario como inactivo
    db.session.commit()  # Guardar cambios en la base de datos
    logout_user()  # Cerrar sesión del usuario
    flash('Tu cuenta ha sido desactivada.', 'info')
    return redirect(url_for('main.home'))  # Redirigir a la página de inicio


@bp.route('/inteligencia-emocional')
@login_required
def inteligencia_emocional_form():
    # Aquí puedes añadir la lógica para el formulario de Inteligencia Emocional
    return render_template('inteligencia_emocional.html', title='Formulario de Inteligencia Emocional')


@bp.route('/ciencia-datos')
@login_required
def ciencia_datos_form():
    try:
        # Construir la ruta al archivo JSON relativa a la ubicación del script actual
        ruta_json = os.path.join(current_app.root_path, 'data', 'data_scientist.json')
        
        # Leer el archivo JSON
        with open(ruta_json, 'r', encoding='utf-8') as file:
            preguntas = json.load(file)
        
        # Log para verificar que las preguntas se cargan correctamente
        current_app.logger.info(f"Preguntas cargadas: {preguntas}")
        
        # Renderizar la plantilla con las preguntas
        return render_template('ciencia-datos.html', title='Test de Ciencia de Datos', preguntas=preguntas)
    
    except FileNotFoundError:
        current_app.logger.error(f"No se pudo encontrar el archivo JSON en {ruta_json}")
        return render_template('error.html', message="No se pudo cargar el test. Por favor, inténtelo más tarde."), 500
    
    except json.JSONDecodeError:
        current_app.logger.error(f"Error al decodificar el archivo JSON en {ruta_json}")
        return render_template('error.html', message="Hubo un problema al cargar el test. Por favor, inténtelo más tarde."), 500


# Función para obtener respuestas del usuario
def obtener_respuestas(form_data, preguntas):
    """
    Procesa las respuestas del formulario y calcula los puntajes para cada disciplina.
    
    :param form_data: Diccionario con los datos del formulario
    :param preguntas: Lista de preguntas del test
    :return: Diccionario con los puntajes acumulados por disciplina
    """
    if not isinstance(form_data, dict) or not isinstance(preguntas, list):
        raise ValueError("Tipos de datos inválidos para form_data o preguntas")

    respuestas = {"estadistica": 0, "aprendizaje_automatico": 0, "analisis_de_datos": 0}
    
    for index, pregunta in enumerate(preguntas):
        respuesta = form_data.get(f"pregunta{index+1}")
        if respuesta and respuesta in pregunta["opciones"]:
            puntajes = pregunta["opciones"][respuesta]["puntajes"]
            for disciplina, puntos in puntajes.items():
                respuestas[disciplina] += puntos
    
    return respuestas

# Función para determinar la disciplina más adecuada
def determinar_disciplina(respuestas: Dict[str, int]) -> str:
    if respuestas:
        disciplina_maxima = max(respuestas, key=respuestas.get)
        if respuestas[disciplina_maxima] >= 40:
            return disciplina_maxima.replace("_", " ").capitalize()
        else:
            return "Busca otra disciplina"
    else:
        return "No se proporcionaron suficientes respuestas para determinar una disciplina"

# Función para mostrar los resultados en una gráfica de barras
def mostrar_grafica(respuestas: Dict[str, int]) -> str:
    disciplinas = list(respuestas.keys())
    puntajes = list(respuestas.values())
    
    if not puntajes or all(p == 0 for p in puntajes):
    # Retornar una imagen en blanco o un mensaje de error
        return ""  # O generar una imagen de error
    
    fig, ax = plt.subplots()

    # Crear las barras y cambiar su color
    barras = ax.bar(disciplinas, puntajes, color='#1A946F')

    # Agregar etiquetas a las barras
    for barra in barras:
        yval = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2, yval + 5, yval, ha='center', va='bottom')

    ax.set_facecolor('#F2E9D2')  # Cambiar el color de fondo
    fig.patch.set_facecolor('#F2E9D2')  # Cambiar el color de fondo de la figura
    plt.xlabel('Disciplinas', color='#1A946F')
    plt.ylabel('Puntajes', color='#1A946F')
    plt.title('Puntajes por disciplina', color='#1A946F')

    if not puntajes:
            raise ValueError("La lista de puntajes está vacía.")
    # Ajustar los límites del eje y para que haya más espacio entre el puntaje más alto y el borde de la imagen
    plt.ylim(0, max(puntajes) + 10)

    # Guardar la gráfica en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png', facecolor=fig.get_facecolor())
    img.seek(0)

    # Codificar la imagen en base64 y decodificarla a una cadena
    img_str = base64.b64encode(img.read()).decode('utf-8')
    return img_str



@bp.route('/resultados', methods=['POST'])
def resultados():
    """
    Procesa las respuestas del test, calcula los resultados y los visualiza.
    """
    id_dispositivo = str(uuid.uuid4())
    
    try:
        # Obtener puntajes directamente del formulario
        puntajes = {
            'estadistica': int(request.form.get('puntaje_estadistica', 0)),
            'aprendizaje_automatico': int(request.form.get('puntaje_aprendizaje_automatico', 0)),
            'analisis_de_datos': int(request.form.get('puntaje_analisis_de_datos', 0))
        }
        
        disciplina = determinar_disciplina(puntajes)
        grafica = mostrar_grafica(puntajes)
        
        puntaje_maximo = max(puntajes.values())

        # Guardar resultado en la base de datos
        nuevo_resultado = Resultado(
            id_dispositivo=id_dispositivo, 
            disciplina=disciplina,
            puntaje_estadistica=puntajes['estadistica'],
            puntaje_aprendizaje_automatico=puntajes['aprendizaje_automatico'],
            puntaje_analisis_de_datos=puntajes['analisis_de_datos']
        )
        db.session.add(nuevo_resultado)
        db.session.commit()

        current_app.logger.info(f"Resultado guardado exitosamente: {nuevo_resultado}")

        return render_template('resultados.html', 
                               disciplina=disciplina, 
                               grafica=grafica, 
                               puntaje=puntaje_maximo,
                               puntajes_detallados=puntajes)

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al procesar resultados: {str(e)}")
        return render_template('error.html', message="Ocurrió un error al procesar los resultados. Por favor, inténtelo más tarde."), 500


# Ruta para mostrar las estadísticas de los resultados    
@bp.route('/estadisticas')
def estadisticas():
    resultados = Resultado.query.all()
    total_personas = len(resultados)  # Contar el número total de personas
    disciplinas = [resultado.disciplina for resultado in resultados]
    conteo = Counter(disciplinas)
    # Crear una gráfica circular
    fig, ax = plt.subplots()
    ax.pie(conteo.values(), labels=conteo.keys(), autopct='%1.1f%%')
    ax.set_facecolor('#f2e9d2')  # Cambiar el color de fondo
    fig.patch.set_facecolor('#f2e9d2')  # Cambiar el color de fondo de la figura
    # Convertir la gráfica a una imagen PNG en base64
    img = io.BytesIO()
    plt.savefig(img, format='png', facecolor=fig.get_facecolor())
    img.seek(0)
    img_str = base64.b64encode(img.read()).decode('utf-8')
    return render_template('estadisticas.html', img_str=img_str, total_personas=total_personas)
