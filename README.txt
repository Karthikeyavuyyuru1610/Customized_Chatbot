Project: Puter Chatbot — Tutor-Mentor README
Motto: "Build smarter chats — faster, clearer, and kinder to your tokens."

Overview
-
This project is a lightweight web chatbot that uses a free client-side Puter.js integration (which connects to Google AI) for generating assistant replies and a small Flask backend to manage conversation history, roles, and simple API endpoints. It’s designed as a learning and prototyping platform: easy to run locally, explore LLM interaction patterns, and iterate on prompt engineering, context management, and performance tweaks.

Who this README is for
-
This guide is written like a mentor: I’ll explain what each component does, why choices were made, and how you can tune the system for speed and accuracy. If you want me to walk through any code file step-by-step, tell me which file and I’ll explain it line-by-line.

High-level architecture
-
- Frontend (browser): `index.html`, `static/script.js`, `static/style.css`
  - Integrates Puter.js to call the client-side LLM. Handles the chat UI, role selection, message rendering, and UI-side validation/debouncing.
- Backend (server): `app.py`, `main.py`
  - Flask app exposes simple JSON endpoints: `/api/chat`, `/api/save-response`, `/api/history`, `/api/roles`, `/api/set-role`, `/api/status`, `/api/clear`, and context endpoints.
  - `PuterChatbot` in `main.py` prepares compact prompts, applies conversation context, and persists messages via `ChatHistory`.
- Storage: SQLite (simple file DB)
  - Stores messages with basic indexing. Lightweight, fast for local development and small datasets.

How the LLM is used (concise explanation)
-
- Puter.js runs in the browser and sends the prompt (prepared by the frontend) to Google AI (via Puter). That reply is returned to the browser.
- The browser displays the assistant response immediately and fires a non-blocking call to `/api/save-response` to persist the assistant message in the server-side SQLite history.
- The backend is used mainly for persistence, role management, and controlled prompt context generation (when the server prepares system-level prompts or rolls up conversation history).

Why this setup?
-
- Client-side Puter.js allows free and easy access to a strong assistant without an API key, excellent for experimentation.
- A small backend reduces token leakage and centralizes history management, allowing you to change how context is assembled without editing browser code.
- SQLite is zero-config and simple to inspect when learning how messages are structured.

Key design choices that help accuracy and speed
-
- Context window: the code uses a limited number of previous messages (default ~20) to keep prompts compact and reduce latency & token usage.
- Message truncation/summarization: long messages are truncated when added to prompts (so extremely long user inputs don't explode the request size).
- Debouncing: frontend `isLoading` flag to prevent duplicate submissions.
- Asynchronous saves: the UI does not wait for the save to finish, so the user sees replies faster.
- Indexing: database has simple indexes (e.g., by role) for faster history queries.

Running locally (Windows PowerShell)
-
Open PowerShell and run:

```powershell
cd "c:\Users\karth\Downloads\NOV end project\gemini-chatbot"
python app.py
```

Then open http://localhost:5000 in your browser.

To stop the server (PowerShell):

```powershell
Get-Process python | Stop-Process -Force
```

Core files to know
-
- `app.py` — Flask routes and public API.
- `main.py` — `PuterChatbot` and `ChatHistory` logic: preparing prompts, saving messages, and small optimizations (context trimming and truncation).
- `config.py` — System prompts and role definitions.
- `static/script.js` — Frontend app logic, debouncing, Puter.js integration.

Endpoints reference
-
- `POST /api/chat` — send user message (server returns `message`, `model`, `success`).
- `POST /api/save-response` — save assistant response to history.
- `GET /api/history` — fetch saved messages.
- `POST /api/clear` — clear history.
- `GET /api/roles` — list roles.
- `POST /api/set-role` — set active role.
- `GET /api/status` — simple health endpoint.

Troubleshooting tips (common problems)
-
- If you see a `500` on `/api/save-response`, check:
  - That the server is running and reachable at `http://127.0.0.1:5000`.
  - The server logs for stack traces. `app.py` prints errors for debugging.
  - That the browser sends valid JSON `{ "response": "..." }` and the response string is not empty.
- If the frontend looks broken after swapping `script.js`, clear browser cache or open dev tools and check the Console/Network tabs.

How to improve accuracy (practical tips)
-
- Prompt engineering: refine your system prompts in `config.py` and add short examples for behavior you want.
- Context quality: prefer including the most relevant recent messages rather than every message; tune the `limit` in `get_conversation_context`.
- Role tuning: create specialized system prompts for particular tasks (e.g., coding assistant vs. tutor) and test them with short, focused prompts.
- Few-shot examples: include 1–3 short examples in the system prompt for complex tasks.

How to improve speed / scalability (practical tips)
-
- Reduce context length further (e.g., 10–15) for faster responses when memory is less critical.
- Aggregate or summarize older messages into a short summary blob instead of including raw older messages.
- Serve the Flask app behind a production WSGI server (Gunicorn/Waitress) for better concurrency.
- If you outgrow client-side Puter.js, consider batching requests through the server and caching LLM responses.

Next steps I can help with (choose any)
-
- Walk through `main.py` line-by-line and explain each function.
- Add a small unit test harness for `ChatHistory` or a test script to simulate many messages.
- Add a compact admin UI to inspect and prune long messages.
- Help tune system prompts for a specific domain (e.g., Python tutoring), and measure response improvement.

Final mentor note
-
You’ve built a clean sandbox for exploring LLM interactions. Keep experiments small: tweak one thing at a time (context length, truncation, prompt text) and measure change. If you want, I’ll help you A/B test prompt changes and create a short checklist to evaluate accuracy, latency, and token efficiency.

Files created/edited by this step
-
- `README.txt` (this file) — created in project root.

If you want, I can now:
- Commit the new README with a suggested commit message.
- Run a quick local test of the `/api/save-response` endpoint and report output/errors.
- Walk through `main.py` (your current file) and annotate key lines with suggestions.

Tell me which next step you want.