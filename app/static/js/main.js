
// // Función para mostrar la siguiente pregunta
// function nextQuestion(index) {
//     document.getElementById('pregunta' + index).classList.remove('active');
//     var nextQuestion = document.getElementById('pregunta' + (index + 1));
//     if (nextQuestion) {
//         nextQuestion.classList.add('active');
//     } else {
//         document.getElementById('submit-button').style.display = 'block';
//     }
// }

// // Función para iniciar el test
// function startTest() {
//     document.getElementById('intro').classList.remove('active');
//     document.getElementById('pregunta1').classList.add('active');
// }

// // Mostrar la introducción al cargar la página
// window.onload = function () {
//     document.getElementById('intro').classList.add('active');
// }