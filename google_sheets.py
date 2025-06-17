import os
import json
from datetime import datetime

# Configurar HOME para evitar erro do gspread
if not os.environ.get('HOME'):
    os.environ['HOME'] = '/tmp'

import gspread
from google.oauth2.service_account import Credentials

class GoogleSheetsManager:
    def __init__(self, credentials_path=None, spreadsheet_name="Quiz Cidade Cinza - Resultados"):
        """
        Inicializa o gerenciador do Google Sheets
        
        Args:
            credentials_path: Caminho para o arquivo JSON de credenciais da conta de serviço
            spreadsheet_name: Nome da planilha no Google Drive
        """
        self.spreadsheet_name = spreadsheet_name
        self.credentials_path = credentials_path or os.getenv('GOOGLE_CREDENTIALS_PATH')
        self.client = None
        self.spreadsheet = None
        
        # Escopos necessários para acessar Google Sheets e Drive
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa o cliente do Google Sheets"""
        try:
            if self.credentials_path and os.path.exists(self.credentials_path):
                # Usar arquivo de credenciais
                credentials = Credentials.from_service_account_file(
                    self.credentials_path, 
                    scopes=self.scopes
                )
            else:
                # Tentar usar variável de ambiente com JSON
                credentials_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
                if credentials_json:
                    credentials_info = json.loads(credentials_json)
                    credentials = Credentials.from_service_account_info(
                        credentials_info, 
                        scopes=self.scopes
                    )
                else:
                    print("Credenciais do Google não encontradas. Funcionalidade do Google Sheets desabilitada.")
                    return
            
            self.client = gspread.authorize(credentials)
            self._get_or_create_spreadsheet()
            
        except Exception as e:
            print(f"Erro ao inicializar Google Sheets: {e}")
            self.client = None
    
    def _get_or_create_spreadsheet(self):
        """Obtém a planilha existente ou cria uma nova"""
        try:
            # Tentar abrir planilha existente
            self.spreadsheet = self.client.open(self.spreadsheet_name)
            print(f"Planilha '{self.spreadsheet_name}' encontrada.")
        except gspread.SpreadsheetNotFound:
            # Criar nova planilha
            self.spreadsheet = self.client.create(self.spreadsheet_name)
            print(f"Nova planilha '{self.spreadsheet_name}' criada.")
            
            # Configurar cabeçalhos
            self._setup_headers()
    
    def _setup_headers(self):
        """Configura os cabeçalhos da planilha"""
        if not self.spreadsheet:
            return
        
        try:
            worksheet = self.spreadsheet.sheet1
            headers = [
                'Data/Hora Submissão',
                'Nome do Aluno',
                'Turma',
                'Data Informada',
                'Respostas (formato: 1.a, 2.b, etc.)',
                'Nota Final',
                'Acertos',
                'Total de Questões'
            ]
            
            # Inserir cabeçalhos na primeira linha
            worksheet.insert_row(headers, 1)
            
            # Formatar cabeçalhos (negrito)
            worksheet.format('A1:H1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
            })
            
            print("Cabeçalhos configurados na planilha.")
            
        except Exception as e:
            print(f"Erro ao configurar cabeçalhos: {e}")
    
    def add_quiz_result(self, student_data):
        """
        Adiciona um resultado de quiz à planilha
        
        Args:
            student_data: Dicionário com os dados do estudante
        """
        if not self.client or not self.spreadsheet:
            print("Google Sheets não está configurado. Dados não salvos na planilha.")
            return False
        
        try:
            worksheet = self.spreadsheet.sheet1
            
            # Preparar dados para inserção
            row_data = [
                student_data.get('submission_time', datetime.now().isoformat()),
                student_data.get('name', ''),
                student_data.get('class', ''),
                student_data.get('date', ''),
                student_data.get('answers', ''),
                student_data.get('score', 0),
                student_data.get('correct_answers', 0),
                student_data.get('total_questions', 10)
            ]
            
            # Adicionar nova linha
            worksheet.append_row(row_data)
            
            print(f"Resultado adicionado à planilha para {student_data.get('name', 'Aluno')}")
            return True
            
        except Exception as e:
            print(f"Erro ao adicionar resultado à planilha: {e}")
            return False
    
    def get_spreadsheet_url(self):
        """Retorna a URL da planilha"""
        if self.spreadsheet:
            return self.spreadsheet.url
        return None
    
    def is_available(self):
        """Verifica se o Google Sheets está disponível"""
        return self.client is not None and self.spreadsheet is not None

