import os
import sqlite3
import json
from datetime import datetime
from config import SYSTEM_PROMPTS

# Optional OpenAI server-side integration
try:
    import openai
except Exception:
    openai = None


class ChatHistory:
    """Manages conversation history in SQLite database with optimized queries"""
    
    def __init__(self, db_path="chat_history.db"):
        self.db_path = db_path
        self.init_db()
        self._count_cache = 0  # Cache for message count
    
    def init_db(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Add index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_role ON messages(role)
        """)
        conn.commit()
        conn.close()
    
    def add_message(self, role: str, content: str):
        """Add a message to history"""
        # Truncate very long messages to maintain performance
        max_length = 5000
        content = content[:max_length] if len(content) > max_length else content
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (role, content) VALUES (?, ?)",
            (role, content)
        )
        conn.commit()
        conn.close()
        self._count_cache += 1
    
    def get_messages(self, limit: int = None):
        """Get all or limited messages - optimized"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if limit:
            cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,))
        else:
            cursor.execute("SELECT role, content FROM messages ORDER BY id")
        messages = cursor.fetchall()
        conn.close()
        return [{"role": msg[0], "content": msg[1]} for msg in messages]
    
    def get_recent(self, limit: int = 6):
        """Get recent messages in chronological order"""
        messages = self.get_messages(limit)
        return list(reversed(messages))
    
    def clear(self):
        """Clear all messages"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages")
        conn.commit()
        conn.close()
        self._count_cache = 0
    
    def get_count(self):
        """Get total message count - cached"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM messages")
        count = cursor.fetchone()[0]
        conn.close()
        self._count_cache = count
        return count


class PuterChatbot:
    """Puter.js-based chatbot with optimized performance"""
    
    def __init__(self):
        self.history = ChatHistory()
        self.current_role = "assistant"
        self.user_context = {
            "location": "Not set",
            "timezone": "UTC",
            "expertise_level": "general",
        }
        # default model for client-side Puter.js
        self.model = "google/gemini-2.5-flash"
        # server-side OpenAI model (if using OpenAI)
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        if self.openai_key and openai:
            openai.api_key = self.openai_key
    
    def get_system_message(self) -> str:
        """Get current role's system prompt"""
        base_prompt = SYSTEM_PROMPTS.get(self.current_role, SYSTEM_PROMPTS["assistant"])
        # Optimized context format
        context_info = f"\n\n[Context: {self.user_context['expertise_level']} level, {self.user_context['timezone']}]"
        return base_prompt + context_info
    
    def set_role(self, role: str):
        """Set chatbot role"""
        if role in SYSTEM_PROMPTS:
            self.current_role = role
            return True
        return False
    
    def set_context(self, location: str = None, timezone: str = None, expertise_level: str = None):
        """Update user context"""
        if location:
            self.user_context["location"] = location
        if timezone:
            self.user_context["timezone"] = timezone
        if expertise_level:
            self.user_context["expertise_level"] = expertise_level
    
    def get_context(self):
        """Get current user context"""
        return self.user_context
    
    def get_conversation_context(self, limit: int = 20) -> str:
        """Get optimized conversation history - reduced from 50 to 20 for speed"""
        all_messages = self.history.get_messages(limit=None)
        
        if not all_messages:
            return ""
        
        # Keep only last 20 messages for better performance
        if len(all_messages) > limit:
            all_messages = all_messages[-limit:]
        
        # Optimized format - more concise
        context_lines = ["[PREVIOUS CONVERSATION:"]
        for msg in all_messages:
            role = "U" if msg['role'] == 'user' else "A"  # Shortened labels
            # Truncate long messages
            content = msg['content'][:100]  # First 100 chars
            content += "..." if len(msg['content']) > 100 else ""
            context_lines.append(f"{role}: {content}")
        context_lines.append("]")
        
        return "\n".join(context_lines)
    
    def prepare_message(self, user_message: str) -> str:
        """Prepare message with optimized formatting"""
        system_message = self.get_system_message()
        conversation_context = self.get_conversation_context(limit=20)
        
        # More concise format
        full_message = f"{system_message}{conversation_context}\n\nUser: {user_message}"
        return full_message
    
    def chat(self, user_message: str) -> dict:
        """Prepare chat message for client-side processing"""
        self.history.add_message("user", user_message)
        prepared_message = self.prepare_message(user_message)
        # If OpenAI API key is configured, call server-side OpenAI for response
        if self.openai_key and openai:
            try:
                ai_text = self._generate_openai_response(prepared_message)
                # save AI response asynchronously via save_ai_response caller
                self.save_ai_response(ai_text)
                return {"success": True, "message": ai_text, "model": self.openai_model}
            except Exception as e:
                # fallback: return prepared prompt for client-side Puter.js
                return {"success": False, "error": str(e), "message": prepared_message, "model": self.model}

        # Default: return prepared message for client-side LLM
        return {"success": True, "message": prepared_message, "model": self.model}
    
    def save_ai_response(self, response: str):
        """Save AI response to history"""
        self.history.add_message("assistant", response)

    def _generate_openai_response(self, prompt: str, temperature: float = 0.2, max_tokens: int = 512) -> str:
        """Call OpenAI Chat API to generate a response from the prepared prompt.

        We send the system prompt + the prepared prompt as a single user message to keep the call simple.
        """
        if not openai:
            raise RuntimeError("openai package not available")

        # Build messages array: use the system prompt as a system role and send prompt as user content
        system_msg = self.get_system_message()
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ]

        resp = openai.ChatCompletion.create(model=self.openai_model, messages=messages, temperature=temperature, max_tokens=max_tokens)
        # Extract text
        if isinstance(resp, dict) and resp.get("choices"):
            return resp["choices"][0]["message"]["content"].strip()
        # Fallback if response structure differs
        return str(resp)


if __name__ == "__main__":
    # Test the chatbot
    bot = PuterChatbot()
    print("✅ Puter Chatbot initialized successfully!")
    print(f"Model: {bot.model}")
    print("No API key required - using free Puter.js access!")

