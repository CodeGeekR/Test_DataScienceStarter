import os
from typing import Dict, List
import matplotlib.pyplot as plt


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
def obtener_respuestas() -> Dict[str, int]:
    respuestas = {}
    for pregunta in preguntas:
        print(pregunta["texto"])
        for opcion, detalles in pregunta["opciones"].items():
            print(f"{opcion}: {detalles['texto']}")
        respuesta = input("Elige una opción (A/B/C/D): ").lower()
        while respuesta not in pregunta["opciones"]:
            print("Opción inválida, por favor elige una opción entre A y D.")
            respuesta = input("Elige una opción (A/B/C/D): ").lower()
        for disciplina, puntos in pregunta["opciones"][respuesta]["puntajes"].items():
            respuestas[disciplina] = respuestas.get(disciplina, 0) + puntos
    return respuestas

# Función para determinar la disciplina más adecuada
def determinar_disciplina(respuestas: Dict[str, int]) -> str:
    disciplina_maxima = max(respuestas, key=respuestas.get)
    if respuestas[disciplina_maxima] >= 40:
        return disciplina_maxima.replace("_", " ").capitalize()
    else:
        return "Busca otra carrera, la ciencia de datos no es lo tuyo"

# Función para mostrar los resultados en una gráfica de barras
def mostrar_grafica(respuestas: Dict[str, int]):
    disciplinas = list(respuestas.keys())
    puntajes = list(respuestas.values())
    plt.bar(disciplinas, puntajes)
    plt.xlabel('Disciplinas')
    plt.ylabel('Puntajes')
    plt.title('Puntajes por disciplina')
    plt.show()

# Función principal
def main():
    print("Bienvenido al test de afinidad para la ciencia de datos.")
    respuestas = obtener_respuestas()
    disciplina = determinar_disciplina(respuestas)
    print(f"\nSegún tus respuestas, la disciplina de la ciencia de datos que más se ajusta a ti es: {disciplina}")
    mostrar_grafica(respuestas)

if __name__ == "__main__":
    main()