from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from typing import Dict, List
from models import db, Resultado
import json
import uuid
from collections import Counter
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.exc import DatabaseError
import os
import time
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    # Usa la variable de entorno DATABASE_URL para la cadena de conexión de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    return app

app = create_app()


# Función para obtener respuestas del usuario
def obtener_respuestas(form_data, preguntas):
    # Verificar que form_data es un diccionario
    if not isinstance(form_data, dict):
        raise ValueError("form_data debe ser un diccionario")

    # Verificar que preguntas es una lista
    if not isinstance(preguntas, list):
        raise ValueError("preguntas debe ser una lista")

    respuestas = {}
    for index, pregunta in enumerate(preguntas):
        respuesta = form_data.get(f"pregunta{index+1}")
        if respuesta:
            for disciplina, puntos in pregunta["opciones"][respuesta]["puntajes"].items():
                respuestas[disciplina] = respuestas.get(disciplina, 0) + puntos
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

    # Ajustar los límites del eje y para que haya más espacio entre el puntaje más alto y el borde de la imagen
    plt.ylim(0, max(puntajes) + 10)

    # Guardar la gráfica en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png', facecolor=fig.get_facecolor())
    img.seek(0)

    # Codificar la imagen en base64 y decodificarla a una cadena
    img_str = base64.b64encode(img.read()).decode('utf-8')
    return img_str


# Ruta para la página principal con el formulario de preguntas
@app.route('/')
def index():
    # Construir la ruta al archivo JSON relativa a la ubicación del script actual
    ruta_json = os.path.join(os.path.dirname(__file__), 'data', 'data_scientist.json')
    with open(ruta_json, 'r') as file:
        preguntas = json.load(file)
    return render_template('index.html', preguntas=preguntas)

@app.route('/resultados', methods=['POST'])
def resultados():
    id_dispositivo = str(uuid.uuid4())  # Generar un ID único para el dispositivo
    
    # Construir la ruta al archivo JSON relativa a la ubicación del script actual
    ruta_json = os.path.join(os.path.dirname(__file__), 'data', 'data_scientist.json')
    with open(ruta_json, 'r') as file:
        preguntas = json.load(file)
        
    respuestas = obtener_respuestas(request.form, preguntas)
    disciplina = determinar_disciplina(respuestas)
    grafica = mostrar_grafica(respuestas)
    
    # Calcular el puntaje máximo
    puntaje_maximo = max(respuestas.values()) if respuestas else 0

    # Intenta guardar el resultado en la base de datos
    for intento in range(5):  # Intenta 5 veces
        try:
            # Almacenar el resultado en la base de datos
            resultado = Resultado(id_dispositivo=id_dispositivo, disciplina=disciplina)
            db.session.add(resultado)
            db.session.commit()
            break  # Si se guarda con éxito, sale del bucle
        except DatabaseError:
            if intento < 4:  # Si no es el último intento, espera un poco y vuelve a intentarlo
                time.sleep(5)  # Espera 5 segundos
                continue
            else:  # Si es el último intento, lanza la excepción
                raise
        finally:
            # Devuelve la respuesta, independientemente de si se produjo una excepción o no
            return render_template('resultados.html', disciplina=disciplina, grafica=grafica, puntaje=puntaje_maximo)


# Ruta para mostrar las estadísticas de los resultados    
@app.route('/estadisticas')
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

if __name__ == "__main__":
    app.run(debug=True)