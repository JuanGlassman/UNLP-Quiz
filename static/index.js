let questions = {{ questions|safe }};
let currentIndex = 0;

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function showQuestion() {
    if (currentIndex >= questions.length) {
        document.getElementById("quiz-container").innerHTML = "<h2>🎉 ¡Has terminado el quiz!</h2>";
        return;
    }

    let questionObj = questions[currentIndex];
    document.getElementById("question-text").innerText = questionObj.question;

    let optionsContainer = document.getElementById("options-container");
    optionsContainer.innerHTML = "";

    questionObj.options.forEach(option => {
        let btn = document.createElement("button");
        btn.innerText = option;
        btn.onclick = () => checkAnswer(questionObj.question, option);
        btn.classList.add("option-btn");
        optionsContainer.appendChild(btn);
    });

    document.getElementById("result").innerText = "";
    document.getElementById("next-btn").style.display = "none";
}

function checkAnswer(question, answer) {
    let buttons = document.querySelectorAll(".option-btn");
    buttons.forEach(btn => btn.disabled = true);  // Deshabilita todas las opciones

    fetch('{% url "check_answer" %}', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ question: question, answer: answer })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = data.correct ? "✅ Correcto" : "❌ Incorrecto";
        document.getElementById("next-btn").style.display = "block";  // Muestra el botón "Siguiente"
    });
}

function nextQuestion() {
    currentIndex++;
    showQuestion();
}

// Mostrar la primera pregunta al cargar la página
document.addEventListener("DOMContentLoaded", showQuestion);