# AI Study Assistant

This is my first AI-based project built using Python and the OpenRouter API. I created this project to understand how Large Language Models (LLMs) work and how they can be integrated into real applications.

At the moment, the application runs in the terminal and allows users to ask questions and receive responses from an AI model.

## Features

- Ask questions to an AI model
- Secure API key management using a `.env` file
- Simple and organized Python project structure
- OpenRouter API integration

## Technologies Used

- Python
- OpenRouter API
- OpenAI Python SDK
- Git & GitHub
- Visual Studio Code

## Project Structure

```
AI-Study-Assistant/
│
├── backend/
│   ├── app.py
│   ├── chatbot.py
│   └── config.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Getting Started

1. Clone the repository.

```bash
git clone https://github.com/gowthamchowdary-k/AI-Study-Assistant.git
```

2. Install the required packages.

```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your OpenRouter API key.

```
OPENROUTER_API_KEY=your_api_key_here
```

4. Run the application.

```bash
python backend/app.py
```

## Future Plans

I plan to continue improving this project by adding:

- Continuous conversation
- Conversation history
- PDF upload and question answering
- Notes summarization
- Quiz generation
- Flashcards
- Streamlit web interface

## About Me

I'm **Kunta Gowtham Chowdary**, a Computer Science Engineering student at KL University. I'm currently learning AI Engineering, Data Structures & Algorithms, and Java while building projects to improve my practical skills.