from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import json
import os
import random
from datetime import datetime
import csv
import io

# Import student_results functions
from student_results import load_results, save_results

app = Flask(__name__)
CORS(app, origins="*")  # Permitir CORS de qualquer origem

# Configurações
TEACHER_PASSWORD = "Profandre123"

# Dados do quiz (mantido aqui por enquanto, mas pode ser movido para quiz_data.py)
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
        "question": "Como \"Cidade Cinza\" retrata a relação entre os artistas urbanos e o poder público municipal? ",
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

def calculate_question_accuracy_by_class(all_results, quiz_data):
    """
    Calcula o índice de acerto por questão para cada turma.
    Retorna um dicionário onde a chave é o nome da turma e o valor é outro dicionário
    com o ID da questão como chave e a porcentagem de acerto como valor.
    """
    class_question_stats = {} # { 'Turma A': { 'q1_id': { 'correct': 0, 'total': 0 }, ... }, ... }

    # Initialize stats for all questions for all potential classes
    all_class_names = sorted(list(set([r.get('class') for r in all_results if r.get('class')])))

    for class_name in all_class_names:
        class_question_stats[class_name] = {}
        for q in quiz_data:
            class_question_stats[class_name][str(q['id'])] = {'correct': 0, 'total': 0}

    for result in all_results:
        class_name = result.get('class')
        if not class_name:
            continue

        # Use 'answers_details' if available, otherwise try to parse 'answers' (legacy)
        answers_to_process = result.get('answers_details')
        if not answers_to_process:
            # Fallback for older entries that might not have 'answers_details'
            # This parsing is less robust if question options were randomized at submission
            # For this reason, it's better to re-submit quizzes if possible after this change.
            student_answers_str = result.get('answers', '') # e.g., "1.a, 2.c, 3.b"
            student_answers_parsed = {}
            for qa_pair in student_answers_str.split(', '):
                if '.' in qa_pair:
                    q_id, ans_letter = qa_pair.split('.', 1)
                    student_answers_parsed[q_id] = ans_letter
            
            # Reconstruct answers_to_process for legacy entries
            answers_to_process = []
            for question in quiz_data:
                q_id = str(question['id'])
                if q_id in student_answers_parsed:
                    # This part is tricky: we need the *text* of the answer, not just the letter.
                    # If the options were randomized, 'a' might mean different things.
                    # For simplicity, we'll try to map the letter to the current quiz_data options.
                    # This is a potential source of inaccuracy for old data.
                    student_answer_letter = student_answers_parsed[q_id]
                    student_answer_text_from_letter = ''
                    try:
                        # Map letter back to option text using current quiz_data options
                        option_index = ord(student_answer_letter) - ord('a')
                        if 0 <= option_index < len(question['options']):
                            student_answer_text_from_letter = question['options'][option_index]
                    except (ValueError, TypeError):
                        pass # Handle cases where letter is not 'a'-'e' or option_index is out of bounds

                    answers_to_process.append({
                        'question_id': q_id,
                        'student_answer': student_answer_text_from_letter,
                        'correct_answer': question['correct_answer'],
                        'is_correct': (student_answer_text_from_letter == question['correct_answer'])
                    })
        
        if not answers_to_process: # Skip if no valid answers to process
            continue

        for answer_detail in answers_to_process:
            q_id = str(answer_detail['question_id'])
            is_correct = answer_detail['is_correct'] # Use the stored 'is_correct' if available

            if q_id in class_question_stats[class_name]:
                class_question_stats[class_name][q_id]['total'] += 1
                if is_correct:
                    class_question_stats[class_name][q_id]['correct'] += 1

    # Calculate percentages
    accuracy_by_class = {}
    for class_name, q_stats in class_question_stats.items():
        accuracy_by_class[class_name] = {}
        for q_id, stats in q_stats.items():
            if stats['total'] > 0:
                accuracy = (stats['correct'] / stats['total']) * 100
                accuracy_by_class[class_name][q_id] = round(accuracy, 2)
            else:
                accuracy_by_class[class_name][q_id] = 0.0 # No attempts for this question in this class

    return accuracy_by_class

@app.route('/api/quiz', methods=['GET'])
def get_quiz():
    """Retornar perguntas do quiz com randomização"""
    import time
    
    # Usar tempo atual como seed para garantir randomização diferente a cada requisição
    random.seed(time.time())
    
    # Criar cópia dos dados do quiz e randomizar
    randomized_quiz = []
    for question in quiz_data:
        # Criar cópia das opções para cada pergunta
        options = question['options'].copy()
        # Randomizar opções para cada pergunta
        random.shuffle(options)
        
        randomized_question = {
            'id': question['id'],
            'question': question['question'],
            'options': options
        }
        randomized_quiz.append(randomized_question)
    
    # Randomizar ordem das perguntas
    random.shuffle(randomized_quiz)
    
    return jsonify(randomized_quiz)

@app.route('/api/submit', methods=['POST'])
def submit_quiz():
    """Submeter respostas do quiz e calcular pontuação"""
    data = request.get_json()
    
    # Extrair informações do estudante
    student_name = data.get('name', '')
    student_class = data.get('class', '')
    student_date = data.get('date', '')
    answers = data.get('answers', {}) # This 'answers' is a dict of {question_id: student_answer_text}
    
    # Calcular pontuação
    correct_answers = 0
    answers_details = [] # New field to store detailed answer info
    
    for question in quiz_data:
        question_id = str(question['id'])
        student_answer_text = answers.get(question_id, '')
        correct_answer_text = question['correct_answer']
        
        is_correct = (student_answer_text == correct_answer_text)
        if is_correct:
            correct_answers += 1
        
        answers_details.append({
            'question_id': question_id,
            'student_answer': student_answer_text,
            'correct_answer': correct_answer_text,
            'is_correct': is_correct
        })
    
    # Calcular nota final (0-10)
    final_score = round((correct_answers / len(quiz_data)) * 10, 1)
    
    # Criar entrada de resultado
    result_entry = {
        'name': student_name,
        'class': student_class,
        'date': student_date,
        'submission_time': datetime.now().isoformat(),
        'answers_details': answers_details, # Store detailed answers
        'score': final_score,
        'correct_answers': correct_answers,
        'total_questions': len(quiz_data)
    }
    
    # Carregar resultados existentes e adicionar novo
    results = load_results()
    results.append(result_entry)
    save_results(results)
    
    return jsonify({
        'success': True,
        'score': final_score,
        'correct_answers': correct_answers,
        'total_questions': len(quiz_data)
    })

@app.route('/api/teacher/login', methods=['POST'])
def teacher_login():
    """Endpoint de login do professor"""
    data = request.get_json()
    password = data.get('password', '')
    
    if password == TEACHER_PASSWORD:
        return jsonify({'success': True, 'message': 'Login realizado com sucesso'})
    else:
        return jsonify({'success': False, 'message': 'Senha incorreta'}), 401

@app.route('/api/teacher/results', methods=['GET'])
def get_teacher_results():
    """Obter resultados para o professor, agrupados por escola e turma"""
    results = load_results()
    
    # Agrupar por escola e depois por turma
    results_by_school_and_class = {}
    for result in results:
        class_name = result.get('class', 'Turma Desconhecida')
        
        # Tentativa de extrair o nome da escola do nome da turma
        # Ex: "E.E. Antônio Carlos - 1º EM REG 4" -> "E.E. Antônio Carlos"
        # Ou "E.E. José Freire - EJA" -> "E.E. José Freire"
        school_name = "Escola Desconhecida"
        if "E.E. Antônio Carlos" in class_name:
            school_name = "E.E. Antônio Carlos"
        elif "E.E. José Freire" in class_name:
            school_name = "E.E. José Freire"
        # Adicione mais regras se houver outras escolas

        if school_name not in results_by_school_and_class:
            results_by_school_and_class[school_name] = {}
        
        if class_name not in results_by_school_and_class[school_name]:
            results_by_school_and_class[school_name][class_name] = []
        
        results_by_school_and_class[school_name][class_name].append(result)
    
    return jsonify(results_by_school_and_class)

@app.route('/api/teacher/download/<class_name>', methods=['GET'])
def download_class_results(class_name):
    """Baixar resultados de uma turma específica como CSV"""
    results = load_results()
    
    # Filtrar resultados por turma
    class_results = [r for r in results if r.get('class') == class_name]
    
    if not class_results:
        return jsonify({'error': 'Nenhum resultado encontrado para esta turma'}), 404
    
    # Criar conteúdo CSV
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    
    # Escrever cabeçalho
    # Incluir 'is_correct' para cada questão no CSV
    headers = ['Nome', 'Turma', 'Data', 'Nota', 'Acertos', 'Total de Questões', 'Data/Hora de Submissão']
    # Add headers for each question's correctness
    for q in quiz_data:
        headers.append(f"Q{q['id']} - Correta")
        headers.append(f"Q{q['id']} - Resposta Aluno")
        headers.append(f"Q{q['id']} - Resposta Certa")

    writer.writerow(headers)
    
    # Escrever dados
    for result in class_results:
        row = [
            result.get('name', ''),
            result.get('class', ''),
            result.get('date', ''),
            result.get('score', ''),
            result.get('correct_answers', ''),
            result.get('total_questions', ''),
            result.get('submission_time', '')
        ]
        
        # Add question-specific details
        answers_details_map = {ad['question_id']: ad for ad in result.get('answers_details', [])}
        for q in quiz_data:
            q_id = str(q['id'])
            detail = answers_details_map.get(q_id, {})
            row.append('Sim' if detail.get('is_correct') else 'Não')
            row.append(detail.get('student_answer', ''))
            row.append(detail.get('correct_answer', ''))
        
        writer.writerow(row)
    
    # Criar resposta com codificação adequada
    output.seek(0)
    csv_content = output.getvalue()
    
    # Adicionar BOM para abertura correta no Excel
    csv_content = '\ufeff' + csv_content
    
    response = make_response(csv_content.encode('utf-8'))
    response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
    response.headers['Content-Disposition'] = f'attachment; filename=resultados_{class_name}.csv'
    
    return response

@app.route('/api/teacher/question_accuracy', methods=['GET'])
def get_question_accuracy():
    """
    Retorna o índice de acerto por questão para cada turma.
    """
    all_results = load_results()
    accuracy_report = calculate_question_accuracy_by_class(all_results, quiz_data)
    return jsonify(accuracy_report)

@app.route('/api/teacher/download_question_accuracy/<class_name>', methods=['GET'])
def download_question_accuracy(class_name):
    """
    Baixar o índice de acerto por questão de uma turma específica como CSV.
    """
    all_results = load_results()
    accuracy_report = calculate_question_accuracy_by_class(all_results, quiz_data)

    if class_name not in accuracy_report:
        return jsonify({'error': 'Nenhum relatório de acerto por questão encontrado para esta turma'}), 404

    class_accuracy = accuracy_report[class_name]

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)

    # Headers: Question ID, Question Text, Accuracy (%)
    headers = ['ID da Questão', 'Questão', 'Acerto (%)']
    writer.writerow(headers)

    for q in quiz_data:
        q_id = str(q['id'])
        accuracy = class_accuracy.get(q_id, 0.0) # Default to 0.0 if no data

        row = [
            q_id,
            q['question'],
            f"{accuracy:.2f}%"
        ]
        writer.writerow(row)

    output.seek(0)
    csv_content = output.getvalue()
    csv_content = '\ufeff' + csv_content # Add BOM for Excel

    response = make_response(csv_content.encode('utf-8'))
    response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
    response.headers['Content-Disposition'] = f'attachment; filename=acerto_por_questao_{class_name}.csv'

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


