from flask import Flask, render_template, request, jsonify
from config import SYSTEM_PROMPTS, ROLE_CONFIG
from main import PuterChatbot

app = Flask(__name__, template_folder=".", static_folder="static")

# Initialize Chatbot
try:
    chatbot = PuterChatbot()
    print("✅ Chatbot initialized!")
    if chatbot.openai_key:
        print("🔐 OpenAI API key detected - using server-side OpenAI integration")
    else:
        print("🎉 Using client-side Puter.js / Gemini (no OpenAI API key detected)")
except Exception as e:
    print(f"❌ Error: {e}")
    chatbot = None


@app.route("/")
def index():
    """Serve main chat interface"""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle chat messages"""
    if not chatbot:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    try:
        data = request.json
        user_message = data.get("message", "").strip()
        
        if not user_message or len(user_message) < 1:
            return jsonify({"error": "Empty message"}), 400
        
        # Prepare message for Puter.js
        result = chatbot.chat(user_message)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/save-response", methods=["POST"])
def save_response():
    """Save AI response to history"""
    if not chatbot:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "No JSON data"}), 400
            
        ai_response = data.get("response", "").strip()
        
        if not ai_response or len(ai_response) < 1:
            return jsonify({"error": "Empty response"}), 400
        
        # Safely save the response
        try:
            chatbot.save_ai_response(ai_response)
        except Exception as save_err:
            print(f"⚠️ Save error: {save_err}")
            return jsonify({"error": f"Failed to save: {str(save_err)}"}), 500
        
        return jsonify({"status": "success"}), 200
    
    except Exception as e:
        print(f"⚠️ Response endpoint error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/history", methods=["GET"])
def get_history():
    """Get chat history"""
    if not chatbot:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    try:
        messages = chatbot.history.get_messages()
        return jsonify({"messages": messages}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/clear", methods=["POST"])
def clear_history():
    """Clear chat history"""
    if not chatbot:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    try:
        chatbot.history.clear()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/status", methods=["GET"])
def status():
    """Check API status"""
    try:
        model = getattr(chatbot, 'openai_model', None) if chatbot else None
        if chatbot and chatbot.openai_key:
            reported_model = chatbot.openai_model
        else:
            reported_model = chatbot.model if chatbot else "unknown"
        return jsonify({"status": "connected", "model": reported_model}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/roles", methods=["GET"])
def get_roles():
    """Get available roles"""
    return jsonify({"roles": list(SYSTEM_PROMPTS.keys()), "config": ROLE_CONFIG}), 200


@app.route("/api/set-role", methods=["POST"])
def set_role():
    """Set chatbot role"""
    if not chatbot:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    try:
        data = request.json
        role = data.get("role", "assistant")
        
        if chatbot.set_role(role):
            return jsonify({"status": "success", "role": role}), 200
        return jsonify({"error": "Invalid role"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/set-context", methods=["POST"])
def set_context():
    """Set user context"""
    if not chatbot:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    try:
        data = request.json
        chatbot.set_context(
            location=data.get("location"),
            timezone=data.get("timezone"),
            expertise_level=data.get("expertise_level")
        )
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/get-context", methods=["GET"])
def get_context():
    """Get user context"""
    if not chatbot:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    try:
        return jsonify(chatbot.get_context()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("\n🚀 Starting Chatbot Server...")
    print("📱 Open: http://localhost:5000")
    app.run(debug=False, threaded=True)
    print("\n🚀 Starting Puter.js Chatbot Web Server...")
    print("📱 Open your browser: http://localhost:5000")
    print("✨ Using FREE Google AI - No API key required!")
    print("⏹️  Press Ctrl+C to stop\n")
    app.run(debug=False, host="localhost", port=5000)
