<<<<<<< HEAD
# Customized_Chatbot
Full-stack Python chatbot with Flask backend and SQLite conversation memory. Integrates OpenAI GPT for responses, supports role-based system prompts, and a responsive web UI. Optimized for low latency and token efficiency with context-window tuning, async saves, and frontend debouncing Speeds dev workflow, supports local testing
=======
# 🧠 Gemini Chatbot

A powerful, feature-rich chatbot powered by **Google Gemini AI**, with a beautiful web interface, conversation history, and role-based customization.

## Features

✨ **Lightning-Fast Responses** - Google Gemini model processes queries instantly
🎭 **9 Role-Based Modes** - Assistant, Python Expert, Customer Support, Teacher, Tech Writer, Code Reviewer, Business Advisor, Creative Writer, Data Analyst
💾 **Persistent Chat History** - SQLite database stores all conversations
⚙️ **Customizable Settings** - Location, timezone, expertise level context
🎨 **Beautiful UI** - Modern gradient design with animations
📱 **Responsive Design** - Works on desktop, tablet, and mobile
🔐 **Secure API Integration** - Uses official Google Generative AI API

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (free tier available)
- pip (Python package manager)

### Installation

1. **Clone/Download the Project**
   ```bash
   cd gemini-chatbot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get Your API Key**
   - Go to: https://aistudio.google.com/app/apikeys
   - Click "Create API key"
   - Copy your API key (starts with `AIza...`)

4. **Update `.env` File**
   - Open `.env` in the project directory
   - Replace the placeholder with your actual API key:
     ```
     GEMINI_API_KEY=AIzaSyApsPhBm6gon-ywGBOyzwfTdUqwcpMwLJs
     GEMINI_MODEL=gemini-2.0-flash
     ```

5. **Run the Server**
   ```bash
   python app.py
   ```

6. **Open in Browser**
   - Navigate to: http://localhost:5000
   - Status should show "Connected" in green
   - Start chatting!

## Usage

### Selecting a Role

The chatbot comes with 9 pre-configured roles:

| Role | Purpose |
|------|---------|
| **Assistant** | General-purpose helpful assistant |
| **Python Expert** | Code help, best practices, explanations |
| **Customer Support** | Professional, empathetic support |
| **Teacher** | Educational explanations with examples |
| **Tech Writer** | Clear documentation and writing |
| **Code Reviewer** | Code analysis and improvement suggestions |
| **Business Advisor** | Strategic business insights |
| **Creative Writer** | Storytelling and creative content |
| **Data Analyst** | Data interpretation and insights |

### Customizing Context

In **Settings**, you can specify:
- **Location**: Used for location-aware responses
- **Timezone**: For time-based context
- **Expertise Level**: Beginner, Intermediate, Advanced, or Expert

### Chat History

- All conversations are automatically saved to SQLite database
- View history via the 📜 button
- Clear history anytime (cannot be undone)

# Customized_Chatbot

Full-stack Python chatbot with a Flask backend and SQLite conversation memory. Integrates OpenAI GPT (server-side) and supports optional client-side Puter.js / Google Gemini integrations, role-based system prompts, and a responsive web UI. Optimized for low latency and token efficiency with context-window tuning, async saves, and frontend debouncing.

## Features

- Role-based system prompts allowing multiple specialist personas (configurable in `config.py`).
- Persistent conversation memory backed by SQLite.
- REST API for chat, history, role management, and user context.
- Performance optimizations: limited context window, message truncation, DB indexing, async saves.
- Beautiful, responsive frontend (`index.html`, `static/script.js`, `static/style.css`).

## Supported LLM Options

- OpenAI GPT (recommended for production; requires `OPENAI_API_KEY` environment variable).
- Puter.js (client-side integration for free Google AI access where available).
- Optional: Google Gemini via Puter.js or server-side integration (if you have API access).

## Quickstart (Windows PowerShell)

```powershell
cd "c:\Users\karth\Downloads\NOV end project\gemini-chatbot"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Set your OpenAI API key (if using OpenAI):

```powershell
setx OPENAI_API_KEY "sk-..."
```

Run the app:

```powershell
python app.py
```

Open `http://localhost:5000` in your browser.

## Configuration

- `config.py`: system prompts and role definitions.
- `main.py`: `PuterChatbot` and `ChatHistory` logic (context window, truncation, DB interactions).
- `app.py`: Flask endpoints and server logic.

## API Endpoints

- `POST /api/chat` — send user message. Body: `{ "message": "..." }`.
- `POST /api/save-response` — save assistant response. Body: `{ "response": "..." }`.
- `GET /api/history` — returns stored messages.
- `POST /api/clear` — clear history.
- `GET /api/roles` — list roles and UI config.
- `POST /api/set-role` — set active role. Body: `{ "role": "..." }`.
- `GET /api/status` — health/metadata.

## Prompting & Context Handling

- Prompts are assembled from the system prompt (per-role), a compact conversation context (last N messages, default 20), and the current user message.
- To reduce token usage and improve speed, older messages are truncated or summarized and compact labels (`U` / `A`) are used.

## Frontend UX

- `static/script.js` includes debouncing to prevent duplicate submissions, asynchronous response saves, and Enter/Shift+Enter handling for multi-line messages.

## Testing

- Health check:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/status" -Method GET
```
- Save-response test:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/save-response" -Method POST -Body (ConvertTo-Json @{response='Test response'}) -ContentType 'application/json'
```
- Fetch history:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/history" -Method GET
```

## Deploying

- For production, serve Flask with a WSGI server (Waitress/Gunicorn) and secure your API keys.

## Recommended Improvements

- Add user authentication and per-user session IDs.
- Implement summary rollups for older conversation history.
- Add streaming response support in the UI for partial assistant replies.
- Add automated tests for `ChatHistory` and API endpoints.

## Project Structure

```
gemini-chatbot/
├── app.py
├── main.py
├── config.py
├── index.html
├── static/
│   ├── script.js
  └── style.css
├── requirements.txt
├── README.md
└── README.txt
```

---

Built with ❤️ — customize prompts and roles in `config.py` to adapt the assistant to your needs.
