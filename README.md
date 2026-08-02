# AI Study Assistant

AI Study Assistant is an AI-powered learning platform built using **Python, Flask, React, FAISS, and Large Language Models (LLMs)**. This project was developed to understand how Retrieval-Augmented Generation (RAG), vector databases, and modern AI models can be integrated into a real-world educational application.

The application allows users to upload a PDF document, ask questions about its contents, generate study materials, and receive document-grounded responses through an interactive web interface.

---

## Features

- Upload and analyze PDF documents
- Ask questions based on the uploaded PDF
- Retrieval-Augmented Generation (RAG) using FAISS
- AI-powered responses using Gemini or OpenRouter
- Interactive React-based web interface
- Markdown formatted AI responses
- Source document citations
- Conversation history
- Intent-based prompt routing
- Modular AI provider architecture
- Secure API key management using a `.env` file

---

## Technologies Used

### Backend
- Python
- Flask
- FAISS
- Sentence Transformers
- PyPDF
- Google Gemini API
- OpenRouter API

### Frontend
- React
- Vite
- Tailwind CSS
- React Markdown
- KaTeX

### Tools
- Git & GitHub
- Visual Studio Code

---

## Project Structure

```text
AI-Study-Assistant/
│
├── backend/
│   ├── app.py
│   ├── chatbot.py
│   ├── config.py
│   ├── providers/
│   ├── routes/
│   ├── services/
│   ├── rag/
│   ├── formatter/
│   ├── prompts/
│   ├── intent/
│   ├── uploads/
│   └── data/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/gowthamchowdary-k/AI-Study-Assistant.git
```

---

### 2. Navigate to the project

```bash
cd AI-Study-Assistant
```

---

### 3. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

### 4. Install frontend dependencies

```bash
cd ../frontend
npm install
```

---

### 5. Create a `.env` file inside the backend folder

Example:

```env
AI_PROVIDER=gemini

GEMINI_API_KEY=your_gemini_api_key

GEMINI_MODEL=gemini-3.5-flash

OPENROUTER_API_KEY=your_openrouter_api_key
```

---

### 6. Run the backend

```bash
cd backend
python app.py
```

---

### 7. Run the frontend

```bash
cd frontend
npm run dev
```

Open your browser and visit:

```
http://localhost:5173
```

---

## Current Capabilities

- AI-powered PDF Question Answering
- Retrieval-Augmented Generation (RAG)
- Intelligent document retrieval using FAISS
- Single PDF learning workflow
- Source citation support
- Document-grounded responses
- Markdown rendering
- Mathematical formula support
- Modular AI provider system
- Gemini and OpenRouter integration

---

## Future Plans

I plan to continue improving this project by adding:

- Multi-PDF support with intelligent retrieval
- Page-level citations
- Better RAG ranking and reranking
- Flashcard generation
- Quiz and MCQ generation
- Automatic notes summarization
- Study roadmap generation
- PDF highlighting
- Voice interaction
- User authentication
- Cloud deployment

---

## About Me

I'm **Kunta Gowtham Chowdary**, a Computer Science Engineering student at **KL University**. I'm passionate about Artificial Intelligence, Large Language Models (LLMs), Backend Development, and Full-Stack Development. I enjoy building real-world AI applications that solve practical problems while continuously improving my software engineering skills.

---

## License

This project is developed for educational and learning purposes.