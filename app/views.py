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
import logging

# Configurar el registro de errores
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Crear un Blueprint llamado 'main' para organizar las rutas de la aplicación
bp = Blueprint('main', __name__)

# Definir la ruta para la página principal y la página de inicio
@bp.route('/')
@bp.route('/home')
def home():
    """
    Función de vista para la página de inicio.
    Renderiza la plantilla 'home.html'.
    """
    return render_template('home.html')

# Definir la ruta para el registro de usuarios, permitiendo métodos GET y POST
@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Función de vista para el registro de usuarios.
    Maneja tanto solicitudes GET como POST.
    """
    # Si el usuario ya está autenticado, redirigir a la página de inicio
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # Crear una instancia del formulario de registro
    form = RegistrationForm()
    
    # Si el formulario es válido al enviarse
    if form.validate_on_submit():
        try:
            # Verificar si el nombre de usuario o el correo electrónico ya existen en la base de datos
            existing_user = Usuario.query.filter(
                (Usuario.username == form.username.data) | (Usuario.email == form.email.data)
            ).first()
            
            if existing_user:
                # Si el usuario ya existe, mostrar un mensaje de error
                flash('El nombre de usuario o el correo electrónico ya están en uso. Por favor, elige otros.', 'danger')
            else:
                # Si el usuario no existe, crear un nuevo usuario
                user = Usuario(username=form.username.data, email=form.email.data)
                user.set_password(form.password.data)  # Establecer la contraseña del usuario
                db.session.add(user)  # Agregar el usuario a la sesión de la base de datos
                db.session.commit()  # Confirmar los cambios en la base de datos
                flash('Tu cuenta ha sido creada exitosamente!', 'success')
                return redirect(url_for('main.login'))  # Redirigir a la página de inicio de sesión
        except Exception as e:
            # Registrar cualquier error que ocurra durante el registro
            logger.error(f"Error en el registro: {e}")
            flash('Ocurrió un error en el registro. Por favor, inténtelo de nuevo más tarde.', 'danger')
    
    # Renderizar la plantilla de registro con el formulario
    return render_template('register.html', title='Registro', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Función de vista para el inicio de sesión de usuarios.
    Maneja tanto solicitudes GET como POST.
    """
    # Si el usuario ya está autenticado, redirigir al menú principal
    if current_user.is_authenticated:
        return redirect(url_for('main.menu'))
    
    # Crear una instancia del formulario de inicio de sesión
    form = LoginForm()
    
    # Si el formulario es válido al enviarse
    if form.validate_on_submit():
        # Buscar al usuario en la base de datos por su correo electrónico
        user = Usuario.query.filter_by(email=form.email.data).first()
        
        # Verificar si el usuario existe y la contraseña es correcta
        if user and user.check_password(form.password.data):
            # Iniciar sesión del usuario
            login_user(user)
            # Obtener la página siguiente a la que redirigir, si existe
            next_page = request.args.get('next')
            # Redirigir a la página siguiente o al menú principal
            return redirect(next_page) if next_page else redirect(url_for('main.menu'))
        else:
            # Mostrar un mensaje de error si el inicio de sesión falla
            flash('Login fallido. Por favor, verifica tu email y contraseña', 'danger')
    
    # Renderizar la plantilla de inicio de sesión con el formulario
    return render_template('login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    """
    Función de vista para cerrar sesión del usuario.
    """
    # Cerrar sesión del usuario
    logout_user()
    # Redirigir a la página de inicio
    return redirect(url_for('main.home'))

@bp.route('/menu')
@login_required
def menu():
    """
    Función de vista para el menú principal.
    Requiere que el usuario esté autenticado.
    """
    # Renderizar la plantilla del menú principal
    return render_template('menu.html', title='Menu')

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Función de vista para el perfil del usuario.
    Maneja tanto solicitudes GET como POST.
    Requiere que el usuario esté autenticado.
    """
    # Crear una instancia del formulario de actualización de perfil
    form = UpdateProfileForm()
    
    # Si el formulario es válido al enviarse
    if form.validate_on_submit():
        # Actualizar los datos del perfil del usuario actual
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        # Guardar los cambios en la base de datos
        db.session.commit()
        # Mostrar un mensaje de éxito
        flash('Tu perfil ha sido actualizado!', 'success')
        # Redirigir a la página del perfil
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        # Si la solicitud es GET, rellenar el formulario con los datos actuales del usuario
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    
    # Renderizar la plantilla del perfil con el formulario
    return render_template('profile.html', title='Perfil', form=form)

@bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    """
    Función de vista para eliminar la cuenta del usuario.
    Requiere que el usuario esté autenticado.
    """
    # Marcar al usuario como inactivo
    current_user.activo = False
    # Guardar los cambios en la base de datos
    db.session.commit()
    # Cerrar sesión del usuario
    logout_user()
    # Mostrar un mensaje informativo
    flash('Tu cuenta ha sido desactivada.', 'info')
    # Redirigir a la página de inicio
    return redirect(url_for('main.home'))


@bp.route('/inteligencia-emocional')
@login_required
def inteligencia_emocional_form():
    """
    Función de vista para mostrar el formulario de inteligencia emocional.
    Requiere que el usuario esté autenticado.
    """
    # Renderiza la plantilla 'inteligencia_emocional.html' con el título especificado
    return render_template('test-inteligencia-emocional.html', title='Test de Inteligencia Emocional')


@bp.route('/ciencia-datos')
@login_required
def ciencia_datos_form():
    """
    Función de vista para mostrar el test de ciencia de datos.
    Requiere que el usuario esté autenticado.
    """
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
        # Log de error si el archivo JSON no se encuentra
        current_app.logger.error(f"No se pudo encontrar el archivo JSON en {ruta_json}")
        # Renderizar una plantilla de error con un mensaje adecuado y devolver un código de estado 500
        return render_template('error.html', message="No se pudo cargar el test. Por favor, inténtelo más tarde."), 500
    
    except json.JSONDecodeError:
        # Log de error si hay un problema al decodificar el archivo JSON
        current_app.logger.error(f"Error al decodificar el archivo JSON en {ruta_json}")
        # Renderizar una plantilla de error con un mensaje adecuado y devolver un código de estado 500
        return render_template('error.html', message="Hubo un problema al cargar el test. Por favor, inténtelo más tarde."), 500


# Función para obtener respuestas del usuario
def obtener_respuestas(form_data, preguntas):
    """
    Procesa las respuestas del formulario y calcula los puntajes para cada disciplina.
    
    :param form_data: Diccionario con los datos del formulario
    :param preguntas: Lista de preguntas del test
    :return: Diccionario con los puntajes acumulados por disciplina
    """
    # Verificar que los parámetros sean del tipo esperado
    if not isinstance(form_data, dict) or not isinstance(preguntas, list):
        raise ValueError("Tipos de datos inválidos para form_data o preguntas")

    # Inicializar un diccionario para almacenar los puntajes por disciplina
    respuestas = {"estadistica": 0, "aprendizaje_automatico": 0, "analisis_de_datos": 0}
    
    # Iterar sobre las preguntas y sus respuestas correspondientes
    for index, pregunta in enumerate(preguntas):
        # Obtener la respuesta del formulario para la pregunta actual
        respuesta = form_data.get(f"pregunta{index+1}")
        # Verificar que la respuesta exista y sea válida
        if respuesta and respuesta in pregunta["opciones"]:
            # Obtener los puntajes asociados a la respuesta
            puntajes = pregunta["opciones"][respuesta]["puntajes"]
            # Sumar los puntajes a las disciplinas correspondientes
            for disciplina, puntos in puntajes.items():
                respuestas[disciplina] += puntos
    
    # Devolver el diccionario con los puntajes acumulados por disciplina
    return respuestas

# Función para determinar la disciplina más adecuada
def determinar_disciplina(respuestas: Dict[str, int]) -> str:
    """
    Determina la disciplina más adecuada basada en los puntajes obtenidos.
    
    :param respuestas: Diccionario con los puntajes acumulados por disciplina
    :return: Nombre de la disciplina más adecuada o un mensaje indicando que no se encontró una disciplina adecuada
    """
    # Verificar que el diccionario de respuestas no esté vacío
    if respuestas:
        # Encontrar la disciplina con el puntaje más alto
        disciplina_maxima = max(respuestas, key=respuestas.get)
        # Verificar si el puntaje más alto es suficiente para determinar una disciplina
        if respuestas[disciplina_maxima] >= 40:
            # Devolver el nombre de la disciplina con el formato adecuado
            return disciplina_maxima.replace("_", " ").capitalize()
        else:
            # Devolver un mensaje indicando que no se encontró una disciplina adecuada
            return "Busca otra disciplina"
    else:
        # Devolver un mensaje indicando que no se proporcionaron suficientes respuestas
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