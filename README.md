# AI Study Assistant

AI Study Assistant is a production-ready, AI-powered learning platform built using **Python, Flask, React, FAISS, and Large Language Models (LLMs)**. The application allows students to securely sign up, upload various study materials (PDFs, DOCX, PPTX, TXT, and Images), and interact with them in real time. 

Powered by a modular RAG (Retrieval-Augmented Generation) pipeline, the assistant automatically handles file parsing, local chunking, embedding generation, and vector database retrieval, ensuring all responses are strictly grounded in user-supplied documents.

---

## 🚀 Key Features

* **Multi-Format Ingestion**: Native parsing for **PDFs**, Word Documents (**DOCX**), PowerPoint Presentations (**PPTX**), plain Text (**TXT**), and Images (**PNG, JPG, JPEG, WEBP**) using high-quality Gemini API OCR.
* **Multi-Document Support**: Upload and chat with multiple files simultaneously. Ask cross-document comparative questions or build a unified study guide.
* **Secure User Authentication**: Secure registration, login, and user profile verification powered by JWT tokens, SQLite database persistence, and standard PBKDF2 password hashing.
* **Absolute Session & Data Isolation**: All uploaded documents, chat logs, contexts, and FAISS indices are strictly isolated under user-specific subdirectories (`uploads/{user_id}/` and `data/{user_id}/`).
* **Intent-Based Prompt Routing**: Classifies user queries to generate tailored study aids including interactive MCQs, summaries, chapter notes, comparative sheets, and revision calendars.
* **KaTeX Math & Markdown Rendering**: Complete support for displaying mathematical formulae, code blocks, tables, and blockquotes cleanly in the chat UI.
* **Docker Containerization**: Unified, production-ready Docker Compose orchestration for local hosting and cloud deployment.

---

## 🛠️ Tech Stack

### Backend
* **Python 3.10**
* **Flask** (HTTP Server & API Routing)
* **FAISS** (Local vector database for fast similarity searches)
* **Sentence Transformers** (`all-MiniLM-L6-v2` for generating embeddings)
* **PyPDF**, **python-docx**, **python-pptx** (Document parsers)
* **PyJWT** (Token authentication)
* **Google GenAI SDK** (Image OCR & Gemini 3.5 Flash inference)

### Frontend
* **React 18** (Vite & ES modules)
* **Tailwind CSS** (Modern visual layout)
* **React Markdown** & **KaTeX** (Rich-text rendering)
* **Framer Motion** (Premium animations & transitions)

---

## 📂 Project Structure

```text
AI-Study-Assistant/
│
├── backend/
│   ├── app.py                  # Flask entrypoint
│   ├── auth.py                 # JWT & encryption helpers
│   ├── chatbot.py              # System prompt builder & LLM caller
│   ├── config.py               # Settings & dotenv loaders
│   ├── study_assistant.db      # SQLite production database
│   ├── Dockerfile              # Backend container profile
│   ├── requirements.txt        # Backend dependencies
│   ├── providers/              # Gemini & OpenRouter LLM clients
│   ├── routes/                 # Auth, chat, upload, & document routers
│   ├── services/               # Core business logic (RAG, upload, documents)
│   └── tests/                  # Backend unit test suites
│
├── frontend/
│   ├── src/
│   │   ├── components/         # Message, Sidebar, DocList, CodeBlock
│   │   ├── pages/              # Login, Register, & Dashboard pages
│   │   ├── services/           # Axios-free Fetch helper (injects JWT headers)
│   │   ├── hooks/              # Chat and Document React hooks
│   │   └── App.jsx             # Auth router coordinator
│   ├── Dockerfile              # Multi-stage container (builds Node, runs Nginx)
│   └── package.json            # Frontend packages
│
├── docker-compose.yml          # Container orchestration profile
└── README.md                   # System manual
```

---

## 🚦 Getting Started

### Prerequisites
* [Node.js 18+](https://nodejs.org/)
* [Python 3.10+](https://www.python.org/)
* Gemini API Key or OpenRouter API Key

---

### Method A: Running with Docker (Recommended)

1. Clone the repository and navigate inside:
   ```bash
   git clone https://github.com/gowthamchowdary-k/AI-Study-Assistant.git
   cd AI-Study-Assistant
   ```

2. Create a `.env` file in the root directory:
   ```env
   AI_PROVIDER=gemini
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL=gemini-3.5-flash
   OPENROUTER_API_KEY=your_openrouter_api_key
   JWT_SECRET_KEY=generate_a_secure_random_string_here
   ```

3. Spin up the containers:
   ```bash
   docker-compose up --build
   ```

4. Open your browser and visit:
   `http://localhost`

---

### Method B: Manual Local Setup

#### 1. Backend Configuration
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Linux/macOS:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file inside the `backend` folder (see environment variables below).
5. Run the Flask server:
   ```bash
   python app.py
   ```
   *The API will start running on `http://127.0.0.1:5000`*

#### 2. Frontend Configuration
1. Open a new terminal tab and navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
4. Open the dev URL in your browser:
   `http://localhost:5173`

---

## 🔒 Environment Variables

| Variable | Description | Default | Required |
| :--- | :--- | :--- | :--- |
| `AI_PROVIDER` | Choose model client (`gemini` or `openrouter`) | `openrouter` | Yes |
| `GEMINI_API_KEY` | Official Google AI Studio API key | - | Required if using `gemini` or image OCR |
| `GEMINI_MODEL` | Target Gemini model identifier | `gemini-3.5-flash` | No |
| `OPENROUTER_API_KEY` | OpenRouter client authorization key | - | Required if using `openrouter` |
| `JWT_SECRET_KEY` | Secret key used to sign session cookies | `study-assistant-super-jwt-secret-key-2026` | No (Recommended in production) |
| `VITE_API_URL` | Frontend pointer to API server | `http://127.0.0.1:5000` | No |

---

## 🧪 Testing

Execute the backend unit test suite:
```bash
cd backend
python -m unittest discover -s tests -p "test_*.py"
```

To compile the React frontend bundle for production checks:
```bash
cd frontend
npm run build
```

---

## 📄 License

This project is developed for educational and learning purposes.