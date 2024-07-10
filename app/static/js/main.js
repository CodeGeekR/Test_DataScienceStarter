
// // Mostrar el loader
// function showLoader() {
//     document.getElementById('loader').style.display = 'block';
// }

// // Ocultar el loader
// function hideLoader() {
//     document.getElementById('loader').style.display = 'none';
// }

// // Función para reintentar la solicitud al servidor
// async function retryRequest(url, options = {}, retries = 5, delay = 2000) {
//     for (let i = 0; i < retries; i++) {
//         try {
//             const response = await fetch(url, options);
//             if (response.ok) {
//                 hideLoader();
//                 return response;
//             }
//         } catch (error) {
//             console.error('Error en la solicitud:', error);
//         }
//         await new Promise(resolve => setTimeout(resolve, delay));
//     }
//     hideLoader();
//     throw new Error('No se pudo completar la solicitud después de varios intentos.');
// }

// // Ejemplo de uso
// document.addEventListener('DOMContentLoaded', () => {
//     const someButton = document.getElementById('someButton');
//     if (someButton) {
//         someButton.addEventListener('click', async () => {
//             showLoader();
//             try {
//                 const response = await retryRequest('/some-endpoint');
//                 const data = await response.json();
//                 console.log('Datos recibidos:', data);
//             } catch (error) {
//                 console.error('Error al obtener los datos:', error);
//             }
//         });
//     }
// });

// Función para mostrar la siguiente pregunta
function nextQuestion(index) {
    document.getElementById('pregunta' + index).classList.remove('active');
    var nextQuestion = document.getElementById('pregunta' + (index + 1));
    if (nextQuestion) {
        nextQuestion.classList.add('active');
    } else {
        document.getElementById('submit-button').style.display = 'block';
    }
}

// Función para iniciar el test
function startTest() {
    document.getElementById('intro').classList.remove('active');
    document.getElementById('pregunta1').classList.add('active');
}

// Mostrar la introducción al cargar la página
window.onload = function () {
    document.getElementById('intro').classList.add('active');
}