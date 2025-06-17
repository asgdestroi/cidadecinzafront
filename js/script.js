// Configuração da API
const API_CONFIG = {
    // Para desenvolvimento local
    development: 'http://localhost:5000',
    // Para produção - substitua pela URL do seu backend hospedado
    production: 'https://cidadecinzabackend.onrender.com'
};

// Detectar ambiente baseado no hostname
const isProduction = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1';
const API_BASE_URL = isProduction ? API_CONFIG.production : API_CONFIG.development;

let quizData = [];
let currentQuestion = 0;
let studentAnswers = {};
let studentInfo = {};

// Aguardar carregamento do DOM
document.addEventListener('DOMContentLoaded', function() {
    // Configurar data atual por padrão
    document.getElementById("student-date").valueAsDate = new Date();

    // Submeter formulário de entrada
    document.getElementById("student-form").addEventListener("submit", async function(e) {
        e.preventDefault();
        
        studentInfo = {
            name: document.getElementById("student-name").value,
            class: document.getElementById("student-class").value,
            date: document.getElementById("student-date").value
        };
        
        await loadQuiz();
    });
});

// Carregar quiz do backend
async function loadQuiz() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/quiz`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        quizData = await response.json();
        
        document.getElementById("entry-page").style.display = "none";
        document.getElementById("quiz-page").style.display = "block";
        
        displayQuestion();
    } catch (error) {
        console.error("Error loading quiz:", error);
        alert("Erro ao carregar o quiz. Verifique se o servidor está rodando ou se a URL da API está correta.");
    }
}

// Exibir pergunta atual
function displayQuestion() {
    const question = quizData[currentQuestion];
    const quizContent = document.getElementById("quiz-content");
    
    quizContent.innerHTML = `
        <div class="question-card">
            <div class="question-number">Pergunta ${currentQuestion + 1} de ${quizData.length}</div>
            <div class="question-text">${question.question}</div>
            <img src="images/question_${question.id}.jpg" alt="Imagem da pergunta ${question.id}" class="question-image" onerror="this.style.display='none'">
            <div class="options">
                ${question.options.map((option, index) => `
                    <div class="option">
                        <input type="radio" id="option_${index}" name="question_${question.id}" value="${option}" onchange="saveAnswer(${question.id}, '${option.replace(/'/g, "\\'")}')">
                        <label for="option_${index}">${String.fromCharCode(97 + index)}) ${option}</label>
                    </div>
                `).join("")}
            </div>
        </div>
    `;
    
    // Restaurar resposta se já foi selecionada
    if (studentAnswers[question.id]) {
        const radio = document.querySelector(`input[value="${studentAnswers[question.id]}"]`);
        if (radio) radio.checked = true;
    }
    
    updateProgress();
    updateNavigation();
}

// Salvar resposta
function saveAnswer(questionId, answer) {
    studentAnswers[questionId] = answer;
}

// Próxima pergunta
function nextQuestion() {
    if (currentQuestion < quizData.length - 1) {
        currentQuestion++;
        displayQuestion();
    }
}

// Pergunta anterior
function previousQuestion() {
    if (currentQuestion > 0) {
        currentQuestion--;
        displayQuestion();
    }
}

// Atualizar barra de progresso
function updateProgress() {
    const progress = ((currentQuestion + 1) / quizData.length) * 100;
    document.getElementById("progress-fill").style.width = progress + "%";
}

// Atualizar navegação
function updateNavigation() {
    const prevBtn = document.getElementById("prev-btn");
    const nextBtn = document.getElementById("next-btn");
    const submitBtn = document.getElementById("submit-btn");
    
    prevBtn.style.display = currentQuestion > 0 ? "block" : "none";
    
    if (currentQuestion === quizData.length - 1) {
        nextBtn.style.display = "none";
        submitBtn.style.display = "block";
    } else {
        nextBtn.style.display = "block";
        submitBtn.style.display = "none";
    }
}

// Submeter quiz
async function submitQuiz() {
    // Verificar se todas as perguntas foram respondidas
    const unansweredQuestions = quizData.filter(q => !studentAnswers[q.id]);
    if (unansweredQuestions.length > 0) {
        alert(`Por favor, responda todas as perguntas. Faltam ${unansweredQuestions.length} pergunta(s).`);
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/submit`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                ...studentInfo,
                answers: studentAnswers
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            showResult(result);
        } else {
            alert("Erro ao submeter o quiz.");
        }
    } catch (error) {
        console.error("Error submitting quiz:", error);
        alert("Erro ao submeter o quiz. Verifique sua conexão ou se o servidor está funcionando.");
    }
}

// Mostrar resultado
function showResult(result) {
    document.getElementById("quiz-page").style.display = "none";
    document.getElementById("result-page").style.display = "block";
    
    document.getElementById("final-score").textContent = result.score.toFixed(1);
    document.getElementById("score-details").textContent = `Você acertou ${result.correct_answers} de ${quizData.length} perguntas.`;
}

// Reiniciar quiz
function restartQuiz() {
    currentQuestion = 0;
    studentAnswers = {};
    studentInfo = {};
    document.getElementById("student-form").reset();
    document.getElementById("student-date").valueAsDate = new Date();
    document.getElementById("entry-page").style.display = "block";
    document.getElementById("quiz-page").style.display = "none";
    document.getElementById("result-page").style.display = "none";
}

// Função para a área do professor
function accessTeacherArea() {
    const password = prompt("Digite a senha do professor:");
    if (password === "Profandre123") {
        window.location.href = "teacher_area.html";
    } else if (password !== null) {
        alert("Senha incorreta!");
    }
}

