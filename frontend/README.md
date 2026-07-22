# StudyBuddy — Student Chatbot (React + Vite + Tailwind)

A simple, professional student chatbot UI built as a React component, with a small Vite project wrapped around it so you can run it immediately.

## Run it locally

You'll need [Node.js](https://nodejs.org/) (v18 or newer) installed.

```bash
# 1. Unzip this folder and open a terminal inside it
npm install

# 2. Start the dev server
npm run dev
```

Then open the URL shown in the terminal (usually `http://localhost:5173`).

## Build for production

```bash
npm run build
npm run preview
```

The production-ready files will be output to the `dist/` folder.

## Project structure

```
studybuddy-react/
├── index.html               # Vite entry HTML
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── src/
    ├── main.jsx              # React root
    ├── App.jsx               # Simple wrapper that centers the chatbot
    ├── StudyBuddyChat.jsx    # The chatbot component (all the logic + UI)
    └── index.css             # Tailwind entry point
```

## How responses are generated

`StudyBuddyChat.jsx` uses a small keyword-matching knowledge base (`responseBank`) to simulate chatbot replies for common student topics — study timetables, revision tips, focus tips, note-taking methods, and simple concept explanations — with a friendly fallback for anything else.

## Connecting a real AI backend (optional)

To make StudyBuddy answer using a real AI model instead of the built-in canned responses, replace the `getBotReply()` function inside `src/StudyBuddyChat.jsx` with a call to your chosen chat API (for example, the Anthropic API), sending the user's message and returning the model's reply. No other part of the UI needs to change.

## Customizing

- Colors, spacing, and animations are set with Tailwind utility classes directly in `StudyBuddyChat.jsx`.
- Sidebar quick-suggestions are defined in the `suggestionPrompts` array near the top of the same file.
