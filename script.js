// Configuração da API
const API_CONFIG = {
    // Para desenvolvimento local
    development: 'http://localhost:5000',
    // Para produção - substitua pela URL do seu backend hospedado no Render.com
    production: 'https://cidadecinzafront.onrender.com' // Atualize esta URL com a sua real do Render.com
};

// Detectar ambiente baseado no hostname
const isProduction = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1';
const API_BASE_URL = isProduction ? API_CONFIG.production : API_CONFIG.development;

let quizData = [];
let currentQuestion = 0;
let studentAnswers = {};
let studentInfo = {};

// Elementos das páginas
const entryPage = document.getElementById('entry-page');
const quizPage = document.getElementById('quiz-page');
const resultPage = document.getElementById('result-page');
const teacherLoginPage = document.getElementById('teacher-login-page');
const teacherDashboardPage = document.getElementById('teacher-dashboard-page');

// Funções para controlar a visibilidade das páginas
function showEntryPage() {
    entryPage.style.display = 'block';
    quizPage.style.display = 'none';
    resultPage.style.display = 'none';
    teacherLoginPage.style.display = 'none';
    teacherDashboardPage.style.display = 'none';
}

function showQuizPage() {
    entryPage.style.display = 'none';
    quizPage.style.display = 'block';
    resultPage.style.display = 'none';
    teacherLoginPage.style.display = 'none';
    teacherDashboardPage.style.display = 'none';
}

function showResultPage() {
    entryPage.style.display = 'none';
    quizPage.style.display = 'none';
    resultPage.style.display = 'block';
    teacherLoginPage.style.display = 'none';
    teacherDashboardPage.style.display = 'none';
}

function showTeacherLogin() {
    entryPage.style.display = 'none';
    quizPage.style.display = 'none';
    resultPage.style.display = 'none';
    teacherLoginPage.style.display = 'block';
    teacherDashboardPage.style.display = 'none';
}

function showTeacherDashboard() {
    entryPage.style.display = 'none';
    quizPage.style.display = 'none';
    resultPage.style.display = 'none';
    teacherLoginPage.style.display = 'none';
    teacherDashboardPage.style.display = 'block';
    loadTeacherDashboard(); // Carrega os dados do dashboard ao exibir
}

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

    // Submeter formulário de login do professor
    document.getElementById("teacher-login-form").addEventListener("submit", async function(e) {
        e.preventDefault();
        const password = document.getElementById("teacher-password").value;
        
        try {
            const response = await fetch(`${API_BASE_URL}/api/teacher/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ password: password })
            });
            
            if (response.ok) {
                showTeacherDashboard();
            } else {
                alert("Senha incorreta!");
            }
        } catch (error) {
            console.error("Erro ao fazer login do professor:", error);
            alert("Erro ao tentar login. Verifique a conexão com o servidor.");
        }
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
        
        showQuizPage();
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
        const radio = document.querySelector(`input[name="question_${question.id}"][value="${studentAnswers[question.id]}"]`);
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
    showResultPage();
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
    showEntryPage();
}

// Funções da Área do Professor
async function loadTeacherDashboard() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/teacher/results`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const resultsBySchoolAndClass = await response.json();
        displayTeacherResults(resultsBySchoolAndClass);
    } catch (error) {
        console.error("Erro ao carregar dashboard do professor:", error);
        alert("Erro ao carregar dados do professor. Verifique a conexão com o servidor.");
        showTeacherLogin(); // Volta para o login se houver erro
    }
}

function displayTeacherResults(resultsBySchoolAndClass) {
    const dashboardContent = document.getElementById('results-by-school-class');
    dashboardContent.innerHTML = ''; // Limpa conteúdo anterior

    for (const schoolName in resultsBySchoolAndClass) {
        const schoolDiv = document.createElement('div');
        schoolDiv.className = 'school-section';
        schoolDiv.innerHTML = `<h2>${schoolName}</h2>`;
        dashboardContent.appendChild(schoolDiv);

        for (const className in resultsBySchoolAndClass[schoolName]) {
            const classDiv = document.createElement('div');
            classDiv.className = 'class-section';
            classDiv.innerHTML = `<h3>${className}</h3>`;

            const table = document.createElement('table');
            table.innerHTML = `
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Data</th>
                        <th>Nota</th>
                        <th>Acertos</th>
                        <th>Total</th>
                        <th>Detalhes</th>
                    </tr>
                </thead>
                <tbody>
                </tbody>
            `;
            const tbody = table.querySelector('tbody');

            resultsBySchoolAndClass[schoolName][className].forEach(result => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td>${result.name}</td>
                    <td>${result.date}</td>
                    <td>${result.score.toFixed(1)}</td>
                    <td>${result.correct_answers}</td>
                    <td>${result.total_questions}</td>
                    <td>
                        <button class="btn-small" onclick="showStudentAnswers('${JSON.stringify(result.answers_details).replace(/'/g, "\\'")}')">Ver Respostas</button>
                    </td>
                `;
            });
            classDiv.appendChild(table);

            // Botões de download
            const downloadButtonsDiv = document.createElement('div');
            downloadButtonsDiv.className = 'download-buttons';
            downloadButtonsDiv.innerHTML = `
                <button class="btn-small" onclick="downloadClassResults('${className}')">Download CSV (Resultados)</button>
                <button class="btn-small" onclick="downloadQuestionAccuracy('${className}')">Download CSV (Acerto por Questão)</button>
            `;
            classDiv.appendChild(downloadButtonsDiv);

            dashboardContent.appendChild(classDiv);
        }
    }
}

function showStudentAnswers(answersDetailsJson) {
    const answersDetails = JSON.parse(answersDetailsJson);
    let detailsHtml = '<h4>Respostas do Aluno:</h4><ul>';
    answersDetails.forEach(detail => {
        const status = detail.is_correct ? 'Correta' : 'Incorreta';
        detailsHtml += `<li><strong>Q${detail.question_id}:</strong> Sua resposta: "${detail.student_answer}" (${status}). Resposta correta: "${detail.correct_answer}"</li>`;
    });
    detailsHtml += '</ul>';
    alert(detailsHtml); // Usar um modal mais sofisticado seria melhor aqui
}

async function downloadClassResults(className) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/teacher/download/${className}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `resultados_${className}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error("Erro ao baixar resultados da turma:", error);
        alert("Erro ao baixar resultados. Verifique os logs do servidor.");
    }
}

async function downloadQuestionAccuracy(className) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/teacher/download_question_accuracy/${className}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `acerto_por_questao_${className}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error("Erro ao baixar acerto por questão:", error);
        alert("Erro ao baixar relatório de acerto por questão. Verifique os logs do servidor.");
    }
}


