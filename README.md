# Quiz Cidade Cinza (https://shre.ink/artcont)

Questionário interativo sobre o documentário "Cidade Cinza" desenvolvido para as escolas E.E. Antônio Carlos e E.E. José Freire.

## 📋 Sobre o Projeto

O Quiz Cidade Cinza é uma aplicação web educativa que permite aos alunos responderem questões sobre o documentário "Cidade Cinza", com área administrativa para professores acompanharem os resultados.

### Funcionalidades

- ✅ Quiz interativo com 10 questões sobre o documentário
- ✅ Randomização de perguntas e opções
- ✅ Sistema de pontuação (0-10)
- ✅ Área do professor protegida por senha
- ✅ Exportação de resultados em CSV
- ✅ Interface responsiva para desktop e mobile
- ✅ Integração com Google Sheets (opcional)

### Turmas Configuradas

**E.E. Antônio Carlos:**
- 1º EM REG 1, 2, 3, 4
- 2º EM REG 1, 2, 3, 4
- 3º EM REG 1, 2, 3, 4

**E.E. José Freire:**
- 1º EM REG 4, EJA 1
- 2º EM REG 1, 4, EJA 1
- 3º EM REG 1, 2, 4, 5, EJA 1

## 🚀 Implantação no GitHub Pages

### Pré-requisitos

1. Conta no GitHub
2. Serviço de hospedagem para o backend (Heroku, Render, Vercel, etc.)

### Passo 1: Configurar o Repositório

1. Acesse [GitHub](https://github.com) e faça login
2. Clique em "New repository"
3. Nome do repositório: `quiz-cidade-cinza`
4. Marque como "Public"
5. Inicialize com README
6. Clique em "Create repository"

### Passo 2: Upload dos Arquivos Frontend

1. No repositório criado, clique em "uploading an existing file"
2. Faça upload dos arquivos da pasta `frontend/`:
   - `index.html`
   - `css/style.css`
   - `js/script.js`
   - `images/` (se houver imagens)

### Passo 3: Ativar GitHub Pages

1. Vá em "Settings" do repositório
2. Role até a seção "Pages"
3. Em "Source", selecione "Deploy from a branch"
4. Escolha "main" branch
5. Clique em "Save"
6. Aguarde alguns minutos para o site ficar disponível

### Passo 4: Configurar URL do Backend

Após hospedar o backend, edite o arquivo `js/script.js` e atualize a URL de produção:

```javascript
const API_CONFIG = {
    development: 'http://localhost:5000',
    production: 'https://SEU-BACKEND-HOSPEDADO.herokuapp.com' // Substitua pela URL real
};
```

## 🔧 Hospedagem do Backend

O backend pode ser hospedado em diversos serviços. Veja as instruções específicas na documentação de cada plataforma.

### Arquivos Necessários para o Backend

- `app.py` - Aplicação Flask principal
- `requirements.txt` - Dependências Python
- `Procfile` - Configuração para Heroku
- `wsgi.py` - Ponto de entrada WSGI

## 👨‍🏫 Área do Professor

- **Senha:** `Profandre123`
- **Funcionalidades:**
  - Visualizar resultados por turma
  - Exportar dados em CSV
  - Acompanhar estatísticas gerais

## 📊 Integração com Google Sheets

Para configurar a integração com Google Sheets, consulte o arquivo `CONFIGURACAO_GOOGLE_SHEETS.md`.

## 🛠️ Desenvolvimento Local

### Frontend
1. Abra `index.html` em um navegador
2. O frontend funcionará em modo de desenvolvimento

### Backend
1. Instale as dependências: `pip install -r requirements.txt`
2. Execute: `python app.py`
3. Acesse: `http://localhost:5000`

## 📝 Licença

Este projeto é de uso educacional para as escolas E.E. Antônio Carlos e E.E. José Freire.

## 🤝 Contribuição

Para sugestões ou melhorias, entre em contato com a equipe pedagógica das escolas.

