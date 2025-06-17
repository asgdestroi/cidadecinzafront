from flask import Blueprint, request, jsonify, session, make_response, send_file
import random
import json
import os
import csv
import io
from datetime import datetime
from flask_cors import cross_origin
from ..config import VALID_CLASSES, TEACHER_PASSWORD, DOWNLOAD_DIR, DOWNLOAD_LINK_EXPIRATION, GOOGLE_CREDENTIALS_PATH, GOOGLE_SPREADSHEET_NAME
from ..google_sheets import GoogleSheetsManager

quiz_bp = Blueprint('quiz', __name__)

# Inicializar Google Sheets Manager
sheets_manager = GoogleSheetsManager(
    credentials_path=GOOGLE_CREDENTIALS_PATH,
    spreadsheet_name=GOOGLE_SPREADSHEET_NAME
)

# Quiz data
quiz_data = [
    {
        "id": 1,
        "question": "Qual é a principal diferença entre grafite e pixo, segundo os artistas entrevistados no documentário \"Cidade Cinza\"?",
        "options": [
            "O grafite é sempre feito com permissão enquanto o pixo é sempre ilegal",
            "O grafite é considerado arte enquanto o pixo é visto apenas como vandalismo puro",
            "O grafite prioriza a estética e o apelo visual, já o pixo enfatiza a mensagem e a ocupação do espaço urbano",
            "O grafite utiliza apenas tintas spray profissionais enquanto o pixo usa materiais improvisados",
            "Não existe diferença significativa entre as duas manifestações urbanas"
        ],
        "correct_answer": "O grafite prioriza a estética e o apelo visual, já o pixo enfatiza a mensagem e a ocupação do espaço urbano"
    },
    {
        "id": 2,
        "question": "Como os artistas retratados no documentário justificam o pixo como forma de expressão artística?",
        "options": [
            "Por ser uma técnica mais simples e acessível do que o grafite tradicional",
            "Por representar uma forma de contestação social e afirmação de presença no espaço público",
            "Por ser mais facilmente aceito e compreendido pelo grande público",
            "Por exigir menos habilidade técnica e preparo artístico",
            "Por ser sempre realizado com autorização dos proprietários dos muros"
        ],
        "correct_answer": "Por representar uma forma de contestação social e afirmação de presença no espaço público"
    },
    {
        "id": 3,
        "question": "Qual foi o papel dos irmãos Os Gêmeos no desenvolvimento do grafite em São Paulo, conforme apresentado no documentário?",
        "options": [
            "Foram os pioneiros absolutos na introdução do pixo na cidade",
            "Contribuíram para internacionalizar o grafite brasileiro, dando visibilidade global à cena paulistana",
            "Atuaram como críticos ferrenhos de qualquer forma de arte urbana",
            "Trabalharam exclusivamente em espaços institucionais, nunca em intervenções urbanas",
            "Foram responsáveis diretos pela criminalização do grafite na cidade"
        ],
        "correct_answer": "Contribuíram para internacionalizar o grafite brasileiro, dando visibilidade global à cena paulistana"
    },
    {
        "id": 4,
        "question": "Como \"Cidade Cinza\" retrata a relação entre os artistas urbanos e o poder público municipal?",
        "options": [
            "Mostra uma cooperação constante e harmoniosa entre as partes",
            "Revela um cenário de conflito com períodos de repressão, mas também momentos de reconhecimento oficial",
            "Apresenta uma completa ausência de interferência governamental",
            "Demonstra que todos os artistas foram contratados formalmente pela prefeitura",
            "Indica que a prefeitura apoiava apenas o pixo, nunca o grafite"
        ],
        "correct_answer": "Revela um cenário de conflito com períodos de repressão, mas também momentos de reconhecimento oficial"
    },
    {
        "id": 5,
        "question": "Qual a posição predominante entre os artistas do filme em relação à criminalização do pixo?",
        "options": [
            "Concordam plenamente com sua classificação como ato vandalico",
            "Defendem sua legitimidade como expressão cultural e criticam a repressão sistemática",
            "Acreditam que apenas o grafite deveria ser permitido por lei",
            "Consideram que o pixo só é aceitável em áreas abandonadas",
            "Não manifestam qualquer opinião formada sobre o assunto"
        ],
        "correct_answer": "Defendem sua legitimidade como expressão cultural e criticam a repressão sistemática"
    },
    {
        "id": 6,
        "question": "Qual foi o impacto da Lei Cidade Limpa sobre as manifestações de arte urbana em São Paulo, segundo o documentário?",
        "options": [
            "Estimulou o surgimento de novos artistas de rua",
            "Intensificou a fiscalização e repressão contra qualquer tipo de intervenção urbana",
            "Afetou apenas a publicidade comercial, sem relação com a arte de rua",
            "Transformou o pixo em patrimônio cultural oficial",
            "Na prática, nunca foi implementada de fato"
        ],
        "correct_answer": "Intensificou a fiscalização e repressão contra qualquer tipo de intervenção urbana"
    },
    {
        "id": 7,
        "question": "Como os artistas do filme percebem a inserção do grafite no circuito comercial de arte?",
        "options": [
            "Consideram que isso representa a perda da essência contestadora original",
            "Veem como a única forma legítima de valorização do grafite",
            "Acreditam que o mercado nunca realmente aceitou o grafite como arte",
            "Não fazem distinção entre grafite e pixo no contexto mercadológico",
            "Avaliam que o pixo tem maior valor comercial que o grafite"
        ],
        "correct_answer": "Consideram que isso representa a perda da essência contestadora original"
    },
    {
        "id": 8,
        "question": "O que o documentário revela sobre as tensões entre grafiteiros e pichadores?",
        "options": [
            "Mostra uma convivência sempre pacífica e colaborativa",
            "Expõe rivalidades, com grafiteiros muitas vezes criticando o pixo como vandalismo e pichadores acusando grafiteiros de \"vendidos\"",
            "Indica que todos os grafiteiros também praticam pixo regularmente",
            "Demonstra completa ausência de conflitos entre os grupos",
            "Revela que a polícia sempre mediou positivamente essas relações"
        ],
        "correct_answer": "Expõe rivalidades, com grafiteiros muitas vezes criticando o pixo como vandalismo e pichadores acusando grafiteiros de \"vendidos\""
    },
    {
        "id": 9,
        "question": "Qual é a visão central apresentada pelo documentário sobre o papel da arte urbana na transformação das cidades?",
        "options": [
            "Que ela contribui para piorar a degradação dos centros urbanos",
            "Que grafite e pixo funcionam como formas de resistência e humanização dos espaços cinzentos",
            "Que deveria ser restrita a museus e galerias especializadas",
            "Que não possui qualquer capacidade transformadora real",
            "Que apenas o grafite tem este poder, nunca o pixo"
        ],
        "correct_answer": "Que grafite e pixo funcionam como formas de resistência e humanização dos espaços cinzentos"
    },
    {
        "id": 10,
        "question": "Como os artistas entrevistados em \"Cidade Cinza\" enxergam o futuro dessas manifestações artísticas urbanas?",
        "options": [
            "Acreditam que ambas estão fadadas ao desaparecimento devido à repressão crescente",
            "Preveem que o grafite se tornará a única forma aceita de arte de rua",
            "Percebem que continuarão evoluindo e se adaptando como formas de expressão e resistência",
            "Esperam que o pixo substitua completamente o grafite no cenário urbano",
            "Não demonstram qualquer preocupação ou reflexão sobre o futuro"
        ],
        "correct_answer": "Percebem que continuarão evoluindo e se adaptando como formas de expressão e resistência"
    }
]

# File to store results
RESULTS_FILE = os.path.join(os.path.dirname(__file__), '..', 'database', 'student_results.json')

def load_results():
    """Load existing results from file"""
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_results(results):
    """Save results to file"""
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

@quiz_bp.route('/quiz', methods=['GET'])
def get_quiz():
    """Return randomized quiz questions with fresh randomization each time"""
    import time
    
    # Seed random with current time to ensure different randomization each request
    random.seed(time.time())
    
    # Create a deep copy of quiz data and randomize
    randomized_quiz = []
    for question in quiz_data:
        # Create a fresh copy of options for each question
        options = question['options'].copy()
        # Randomize options for each question
        random.shuffle(options)
        
        randomized_question = {
            'id': question['id'],
            'question': question['question'],
            'options': options
        }
        randomized_quiz.append(randomized_question)
    
    # Randomize question order
    random.shuffle(randomized_quiz)
    
    return jsonify(randomized_quiz)

@quiz_bp.route('/submit', methods=['POST'])
def submit_quiz():
    """Submit quiz answers and calculate score"""
    data = request.get_json()
    
    # Extract student info
    student_name = data.get('name', '')
    student_class = data.get('class', '')
    student_date = data.get('date', '')
    answers = data.get('answers', {})
    
    # Calculate score
    correct_answers = 0
    answer_summary = []
    
    for question in quiz_data:
        question_id = str(question['id'])
        student_answer = answers.get(question_id, '')
        correct_answer = question['correct_answer']
        
        is_correct = student_answer == correct_answer
        if is_correct:
            correct_answers += 1
        
        # Find the option letter (a, b, c, d, e)
        option_letter = ''
        for i, option in enumerate(question['options']):
            if option == student_answer:
                option_letter = chr(ord('a') + i)
                break
        
        answer_summary.append(f"{question['id']}.{option_letter}")
    
    # Calculate final score (0-10)
    final_score = round((correct_answers / len(quiz_data)) * 10, 1)
    
    # Create result entry
    result_entry = {
        'name': student_name,
        'class': student_class,
        'date': student_date,
        'submission_time': datetime.now().isoformat(),
        'answers': ', '.join(answer_summary),
        'score': final_score,
        'correct_answers': correct_answers,
        'total_questions': len(quiz_data)
    }
    
    # Load existing results and add new one
    results = load_results()
    results.append(result_entry)
    save_results(results)
    
    # Salvar no Google Sheets se disponível
    if sheets_manager.is_available():
        sheets_manager.add_quiz_result(result_entry)
    
    return jsonify({
        'success': True,
        'score': final_score,
        'correct_answers': correct_answers,
        'total_questions': len(quiz_data),
        'google_sheets_url': sheets_manager.get_spreadsheet_url() if sheets_manager.is_available() else None
    })

@quiz_bp.route('/results', methods=['GET'])
def get_results():
    """Get all student results (for teacher access)"""
    results = load_results()
    
    # Group by class
    results_by_class = {}
    for result in results:
        class_name = result['class']
        if class_name not in results_by_class:
            results_by_class[class_name] = []
        results_by_class[class_name].append(result)
    
    return jsonify(results_by_class)

# Teacher authentication routes
@quiz_bp.route('/teacher/login', methods=['POST'])
def teacher_login():
    """Teacher login endpoint"""
    data = request.get_json()
    password = data.get('password', '')
    
    if password == TEACHER_PASSWORD:
        session['teacher_authenticated'] = True
        return jsonify({'success': True, 'message': 'Login realizado com sucesso'})
    else:
        return jsonify({'success': False, 'message': 'Senha incorreta'}), 401

@quiz_bp.route('/teacher/logout', methods=['POST'])
def teacher_logout():
    """Teacher logout endpoint"""
    session.pop('teacher_authenticated', None)
    return jsonify({'success': True, 'message': 'Logout realizado com sucesso'})

@quiz_bp.route('/teacher/check', methods=['GET'])
def check_teacher_auth():
    """Check if teacher is authenticated"""
    is_authenticated = session.get('teacher_authenticated', False)
    return jsonify({'authenticated': is_authenticated})

@quiz_bp.route('/teacher/results', methods=['GET'])
def get_teacher_results():
    """Get results for authenticated teacher"""
    if not session.get('teacher_authenticated', False):
        return jsonify({'error': 'Não autorizado'}), 401
    
    results = load_results()
    
    # Group by class
    results_by_class = {}
    for result in results:
        class_name = result['class']
        if class_name not in results_by_class:
            results_by_class[class_name] = []
        results_by_class[class_name].append(result)
    
    return jsonify(results_by_class)

@quiz_bp.route('/teacher/download/<class_name>', methods=['GET'])
def download_class_results(class_name):
    """Download results for a specific class as CSV"""
    if not session.get('teacher_authenticated', False):
        return jsonify({'error': 'Não autorizado'}), 401
    
    results = load_results()
    
    # Filter results by class
    class_results = [r for r in results if r['class'] == class_name]
    
    if not class_results:
        return jsonify({'error': 'Nenhum resultado encontrado para esta turma'}), 404
    
    # Create CSV content with semicolon delimiter for Brazilian Portuguese
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    
    # Write header
    writer.writerow(['Nome', 'Turma', 'Data', 'Respostas', 'Nota', 'Acertos', 'Total de Questões', 'Data/Hora de Submissão'])
    
    # Write data
    for result in class_results:
        writer.writerow([
            result['name'],
            result['class'],
            result['date'],
            result['answers'],
            result['score'],
            result['correct_answers'],
            result['total_questions'],
            result['submission_time']
        ])
    
    # Create response with proper encoding
    output.seek(0)
    csv_content = output.getvalue()
    
    # Add BOM for proper Excel opening in Portuguese
    csv_content = '\ufeff' + csv_content
    
    response = make_response(csv_content.encode('utf-8'))
    response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
    response.headers['Content-Disposition'] = f'attachment; filename=resultados_{class_name}.csv'
    
    return response

@quiz_bp.route('/teacher/download/all', methods=['GET'])
def download_all_results():
    """Download all results as CSV"""
    if not session.get('teacher_authenticated', False):
        return jsonify({'error': 'Não autorizado'}), 401
    
    results = load_results()
    
    if not results:
        return jsonify({'error': 'Nenhum resultado encontrado'}), 404
    
    # Create CSV content with semicolon delimiter for Brazilian Portuguese
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    
    # Write header
    writer.writerow(['Nome', 'Turma', 'Data', 'Respostas', 'Nota', 'Acertos', 'Total de Questões', 'Data/Hora de Submissão'])
    
    # Write data
    for result in results:
        writer.writerow([
            result['name'],
            result['class'],
            result['date'],
            result['answers'],
            result['score'],
            result['correct_answers'],
            result['total_questions'],
            result['submission_time']
        ])
    
    # Create response with proper encoding
    output.seek(0)
    csv_content = output.getvalue()
    
    # Add BOM for proper Excel opening in Portuguese
    csv_content = '\ufeff' + csv_content
    
    response = make_response(csv_content.encode('utf-8'))
    response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
    response.headers['Content-Disposition'] = 'attachment; filename=todos_resultados.csv'
    
    return response

