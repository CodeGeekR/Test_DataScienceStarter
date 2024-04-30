from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from typing import Dict, List
from models import db, Resultado
import uuid
from collections import Counter
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import os
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

# Preguntas y puntajes para cada disciplina
preguntas = [
    {
        "texto": "¿Cómo te gusta trabajar?",
        "opciones": {
            "a": {"texto": "Con instrucciones precisas", "puntajes": {"estadistica": 4, "aprendizaje_automatico": 2, "analisis_de_datos": 2}},
            "b": {"texto": "Resolviendo acertijos", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}},
            "c": {"texto": "Explorando información", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 2, "analisis_de_datos": 4}},
            "d": {"texto": "De forma creativa", "puntajes": {"estadistica": 1, "aprendizaje_automatico": 1, "analisis_de_datos": 4}}
        }
    },
    {
        "texto": "Imagina que tienes que organizar una fiesta de cumpleaños. ¿Qué preferirías?",
        "opciones": {
            "a": {"texto": "Planificar cada detalle minuciosamente para asegurarme de que todo salga perfecto", "puntajes": {"estadistica": 4, "aprendizaje_automatico": 2, "analisis_de_datos": 2}},
            "b": {"texto": "Dejar que una aplicación o programa se encargue de organizar todo automáticamente", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}},
            "c": {"texto": "Improvisar y ajustar los planes según vaya avanzando la organización", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 2, "analisis_de_datos": 4}},
            "d": {"texto": "Hacer un plan general y luego ir explorando nuevas ideas creativas", "puntajes": {"estadistica": 1, "aprendizaje_automatico": 1, "analisis_de_datos": 4}}
        }
    },
    {
    "texto": "Imagina que tienes acceso a datos sobre tus hábitos diarios. ¿Qué te gustaría hacer con esa información?",
    "opciones": {
        "a": {"texto": "Analizarlos para entender mejor mis patrones de comportamiento", "puntajes": {"estadistica": 4, "aprendizaje_automatico": 2, "analisis_de_datos": 2}},
        "b": {"texto": "Usarlos para predecir tendencias futuras en mis actividades", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}},
        "c": {"texto": "Visualizarlos para ver gráficamente cómo varían mis hábitos con el tiempo", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 2, "analisis_de_datos": 4}},
        "d": {"texto": "Utilizarlos para contar historias sobre mi vida y mis decisiones diarias", "puntajes": {"estadistica": 1, "aprendizaje_automatico": 1, "analisis_de_datos": 4}}
    }
    },
    {
        "texto": "Quieres aprender a cocinar un nuevo plato. ¿Cómo te gustaría empezar?",
        "opciones": {
            "a": {"texto": "Seguir meticulosamente una receta paso a paso", "puntajes": {"estadistica": 4, "aprendizaje_automatico": 2, "analisis_de_datos": 1}},
            "b": {"texto": "Usar una aplicación que te guíe en cada paso del proceso", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}},
            "c": {"texto": "Improvisar con los ingredientes y ajustar la receta según tu intuición", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 2, "analisis_de_datos": 4}},
            "d": {"texto": "Experimentar con diferentes técnicas y sabores para crear algo nuevo", "puntajes": {"estadistica": 1, "aprendizaje_automatico": 1, "analisis_de_datos": 4}}
        }
    },
    {
        "texto": "Estás planeando unas vacaciones. ¿Cómo te gustaría organizar tu itinerario?",
        "opciones": {
            "a": {"texto": "Planificar cada día con horarios detallados y actividades específicas", "puntajes": {"estadistica": 4, "aprendizaje_automatico": 2, "analisis_de_datos": 2}},
            "b": {"texto": "Usar una aplicación que te sugiera actividades en función de tus intereses", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}},
            "c": {"texto": "Dejar espacio para la improvisación y decidir sobre la marcha qué hacer cada día", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 2, "analisis_de_datos": 4}},
            "d": {"texto": "Tener un plan general pero estar abierto a cambiar según las circunstancias", "puntajes": {"estadistica": 1, "aprendizaje_automatico": 1, "analisis_de_datos": 4}}
        }
    },
    {
        "texto": "¿Qué prefieres hacer un fin de semana lluvioso?",
        "opciones": {
            "a": {"texto": "Quedarte en casa y leer un libro o ver películas", "puntajes": {"estadistica": 4, "aprendizaje_automatico": 2, "analisis_de_datos": 1}},
            "b": {"texto": "Explorar nuevas series o películas recomendadas por algoritmos de streaming", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}},
            "c": {"texto": "Hacer actividades creativas como cocinar, pintar o escribir", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 2, "analisis_de_datos": 4}},
            "d": {"texto": "Salir a explorar la ciudad sin un plan definido", "puntajes": {"estadistica": 1, "aprendizaje_automatico": 1, "analisis_de_datos": 4}}
        }
    },
    {
        "texto": "¿Qué es lo primero que harías si tuvieras que enseñar a una computadora a reconocer si una imagen es de un gato o un perro?",
        "opciones": {
            "a": {"texto": "Mostrarle muchas imágenes de gatos y perros y decirle cuál es cuál", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}},
            "b": {"texto": "Programar un algoritmo que analice los colores de la imagen", "puntajes": {"estadistica": 3, "aprendizaje_automatico": 2, "analisis_de_datos": 3}},
            "c": {"texto": "Decirle a la computadora que adivine", "puntajes": {"estadistica": 1, "aprendizaje_automatico": 1, "analisis_de_datos": 4}},
            "d": {"texto": "No tengo idea", "puntajes": {"estadistica": 1, "aprendizaje_automatico": 1, "analisis_de_datos": 1}}
        }
    },
        {
        "texto": "¿Qué harías si tuvieras que contar la cantidad de caramelos en un tazón?",
        "opciones": {
            "a": {"texto": "Contarlos uno por uno cuidadosamente para no equivocarme", "puntajes": {"estadistica": 4, "aprendizaje_automatico": 2, "analisis_de_datos": 2}},
            "b": {"texto": "Tratar de adivinar un número aproximado", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}},
            "c": {"texto": "Sacar una muestra del tazón y contar esa muestra para estimar el total", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 2, "analisis_de_datos": 4}},
            "d": {"texto": "Usar una máquina que pueda contar los caramelos automáticamente", "puntajes": {"estadistica": 1, "aprendizaje_automatico": 1, "analisis_de_datos": 4}}
        }
    },
    {
        "texto": "¿Qué harías para predecir si lloverá mañana?",
        "opciones": {
            "a": {"texto": "Mirarías el pronóstico del tiempo", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 2, "analisis_de_datos": 4}},
            "b": {"texto": "Analizarías los datos de lluvia históricos", "puntajes": {"estadistica": 4, "aprendizaje_automatico": 3, "analisis_de_datos": 2}},
            "c": {"texto": "Lanzarías una moneda al aire", "puntajes": {"estadistica": 1, "aprendizaje_automatico": 1, "analisis_de_datos": 1}},
            "d": {"texto": "No estoy seguro", "puntajes": {"estadistica": 1, "aprendizaje_automatico": 1, "analisis_de_datos": 1}}
        }
    },
    {
        "texto": "¿Qué es lo primero que harías si tuvieras que hacer una recomendación de película para alguien?",
        "opciones": {
            "a": {"texto": "Le preguntarías qué género prefiere", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 2, "analisis_de_datos": 4}},
            "b": {"texto": "Analizarías sus películas favoritas", "puntajes": {"estadistica": 3, "aprendizaje_automatico": 3, "analisis_de_datos": 3}},
            "c": {"texto": "Le darías una lista aleatoria", "puntajes": {"estadistica": 1, "aprendizaje_automatico": 1, "analisis_de_datos": 1}},
            "d": {"texto": "No sé", "puntajes": {"estadistica": 1, "aprendizaje_automatico": 1, "analisis_de_datos": 1}}
        }
    },
    {
        "texto": "Si quisieras saber cuál es la altura promedio de tus amigos, ¿qué harías?",
        "opciones": {
            "a": {"texto": "Medirías la altura de cada uno y calcularías la media", "puntajes": {"estadistica": 4, "aprendizaje_automatico": 2, "analisis_de_datos": 2}},
            "b": {"texto": "Adivinarías", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}},
            "c": {"texto": "No me importaría saberlo", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 2, "analisis_de_datos": 3}},
            "d": {"texto": "No estoy seguro", "puntajes": {"estadistica": 1, "aprendizaje_automatico": 1, "analisis_de_datos": 1}}
    }
    },
    {
        "texto": "Imagina que tienes un rompecabezas muy difícil. ¿Qué haces?",
        "opciones": {
            "a": {"texto": "Sigues intentándolo hasta que lo resuelves, sin importar cuánto tiempo te lleve", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 2, "analisis_de_datos": 4}},
            "b": {"texto": "Buscas patrones y sigues un método paso a paso para resolverlo", "puntajes": {"estadistica": 4, "aprendizaje_automatico": 2, "analisis_de_datos": 2}},
            "c": {"texto": "Pruebas diferentes estrategias y te diviertes experimentando", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}},
            "d": {"texto": "Buscas una solución en línea o creas una herramienta para resolverlo automáticamente", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}}
    }
    },
    {
        "texto": "Si pudieras tener un superpoder, ¿cuál elegirías?",
        "opciones": {
            "a": {"texto": "La habilidad de predecir el futuro con precisión", "puntajes": {"estadistica": 4, "aprendizaje_automatico": 2, "analisis_de_datos": 2}},
            "b": {"texto": "La habilidad de entender y analizar cualquier tipo de información", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 2, "analisis_de_datos": 4}},
            "c": {"texto": "La habilidad de crear cualquier cosa que imagines", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}},
            "d": {"texto": "La habilidad de automatizar cualquier tarea aburrida", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}}
    }
    },
    {
        "texto": "¿Qué tipo de películas o series te gustan más?",
        "opciones": {
            "a": {"texto": "Documentales y programas de investigación", "puntajes": {"estadistica": 4, "aprendizaje_automatico": 2, "analisis_de_datos": 2}},
            "b": {"texto": "Series de detectives y crímenes", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 2, "analisis_de_datos": 4}},
            "c": {"texto": "Películas de ciencia ficción y fantasía", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}},
            "d": {"texto": "Programas sobre tecnología e innovación", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}}
    }
    },
    {
        "texto": "¿Qué materia escolar te gusta más?",
        "opciones": {
            "a": {"texto": "Matemáticas o física", "puntajes": {"estadistica": 4, "aprendizaje_automatico": 2, "analisis_de_datos": 2}},
            "b": {"texto": "Ciencias sociales o historia", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 2, "analisis_de_datos": 4}},
            "c": {"texto": "Arte o música", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}},
            "d": {"texto": "Informática o tecnología", "puntajes": {"estadistica": 2, "aprendizaje_automatico": 4, "analisis_de_datos": 2}}
    }
    }
]

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
    ax.bar(disciplinas, puntajes)
    ax.set_facecolor('#f2e9d2')  # Cambiar el color de fondo
    fig.patch.set_facecolor('#f2e9d2')  # Cambiar el color de fondo de la figura
    plt.xlabel('Disciplinas')
    plt.ylabel('Puntajes')
    plt.title('Puntajes por disciplina')
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
    return render_template('index.html', preguntas=preguntas)

# Ruta para procesar el formulario y mostrar los resultados
@app.route('/resultados', methods=['POST'])
def resultados():
    try:
        id_dispositivo = str(uuid.uuid4())  # Generar un ID único para el dispositivo
        respuestas = obtener_respuestas(request.form, preguntas)
        disciplina = determinar_disciplina(respuestas)
        grafica = mostrar_grafica(respuestas)
        # Almacenar el resultado en la base de datos
        resultado = Resultado(id_dispositivo=id_dispositivo, disciplina=disciplina)
        db.session.add(resultado)
        db.session.commit()
        return render_template('resultados.html', disciplina=disciplina, grafica=grafica)
    except Exception as e:
        return str(e)
    
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