from flask import Flask, render_template, request, jsonify, session
from src.rag_agent import ask
import re
import datetime
import uuid
import json
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# In-memory storage for chat sessions (use database in production)
chat_sessions = {}

def clean_response(text: str) -> str:
    """Clean markdown and format response for HTML display."""
    # Convert markdown to HTML-like formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)  # bold
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)              # italics
    text = text.replace("\n", "<br>")                              # line breaks
    text = text.replace("\u2022", "•")                             # bullet points
    
    # Format numbered lists
    text = re.sub(r'(\d+\.\s*)', r'<br>\1', text)
    text = re.sub(r'(\*\s*)', r'<br>• ', text)
    
    return text.strip()

def get_session_id():
    """Get or create session ID"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def get_chat_history(session_id):
    """Get chat history for session"""
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    return chat_sessions[session_id]

def add_to_chat_history(session_id, sender, message, message_type="text"):
    """Add message to chat history"""
    timestamp = datetime.datetime.now().strftime("%I:%M %p")
    message_data = {
        "id": str(uuid.uuid4()),
        "sender": sender,
        "message": message,
        "timestamp": timestamp,
        "type": message_type
    }
    
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    chat_sessions[session_id].append(message_data)
    return message_data

def get_health_suggestions(user_input):
    """Get contextual health suggestions"""
    suggestions = []
    input_lower = user_input.lower()
    
    if any(word in input_lower for word in ["headache", "head", "pain"]):
        suggestions = [
            "What are common headache triggers?",
            "How to relieve tension headaches?",
            "When should I see a doctor for headaches?"
        ]
    elif any(word in input_lower for word in ["fever", "temperature", "hot"]):
        suggestions = [
            "How to reduce fever naturally?",
            "What temperature is considered high fever?",
            "Home remedies for fever relief"
        ]
    elif any(word in input_lower for word in ["cough", "cold", "flu"]):
        suggestions = [
            "Best remedies for persistent cough",
            "How to boost immune system?",
            "Difference between cold and flu"
        ]
    else:
        suggestions = [
            "What are healthy lifestyle tips?",
            "How often should I exercise?",
            "What foods boost immunity?"
        ]
    
    return suggestions

@app.route("/")
def index():
    session_id = get_session_id()
    chat_history = get_chat_history(session_id)
    
    # Add welcome message if it's a new session
    if not chat_history:
        welcome_msg = """
        👋 Hello! I'm Dr. HealthMate, your AI medical assistant. 
        <br><br>
        I can help you with:
        <br>• General health questions
        <br>• Symptom information
        <br>• Medication guidance
        <br>• Health tips and advice
        <br><br>
        <strong>⚠️ Disclaimer:</strong> I provide general information only. 
        Always consult healthcare professionals for medical emergencies or serious concerns.
        <br><br>
        What health question can I help you with today?
        """
        add_to_chat_history(session_id, "Dr. HealthMate", welcome_msg)
        chat_history = get_chat_history(session_id)
    
    return render_template("index.html", chat_history=chat_history)

@app.route("/ask", methods=["POST"])
def ask_question():
    session_id = get_session_id()
    user_input = request.json.get("message", "").strip()
    
    if not user_input:
        return jsonify({"error": "Empty message"}), 400
    
    # Add user message to history
    user_message = add_to_chat_history(session_id, "You", user_input)
    
    try:
        # Get AI response
        response = ask(user_input)
        cleaned_response = clean_response(response)
        
        # Add bot response to history
        bot_message = add_to_chat_history(session_id, "Dr. HealthMate", cleaned_response)
        
        # Get contextual suggestions
        suggestions = get_health_suggestions(user_input)
        
        return jsonify({
            "user_message": user_message,
            "bot_message": bot_message,
            "suggestions": suggestions,
            "success": True
        })
        
    except Exception as e:
        error_msg = f"⚠️ I'm experiencing technical difficulties. Please try again in a moment."
        bot_message = add_to_chat_history(session_id, "Dr. HealthMate", error_msg)
        
        return jsonify({
            "user_message": user_message,
            "bot_message": bot_message,
            "suggestions": [],
            "success": False,
            "error": str(e)
        })

@app.route("/clear_chat", methods=["POST"])
def clear_chat():
    session_id = get_session_id()
    if session_id in chat_sessions:
        chat_sessions[session_id] = []
    return jsonify({"success": True})

@app.route("/export_chat", methods=["GET"])
def export_chat():
    session_id = get_session_id()
    chat_history = get_chat_history(session_id)
    
    # Create text export
    export_text = f"Dr. HealthMate Chat Export\n"
    export_text += f"Date: {datetime.datetime.now().strftime('%B %d, %Y')}\n"
    export_text += "=" * 50 + "\n\n"
    
    for msg in chat_history:
        clean_msg = re.sub(r'<[^>]+>', '', msg['message'])  # Remove HTML tags
        export_text += f"[{msg['timestamp']}] {msg['sender']}: {clean_msg}\n\n"
    
    return jsonify({
        "export_text": export_text,
        "filename": f"healthmate_chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    })

@app.route("/quick_actions", methods=["GET"])
def quick_actions():
    actions = [
        {"text": "Check symptoms", "icon": "🔍"},
        {"text": "Medication info", "icon": "💊"},
        {"text": "Health tips", "icon": "💡"},
        {"text": "Exercise advice", "icon": "🏃‍♂️"},
        {"text": "Nutrition guide", "icon": "🥗"},
        {"text": "Mental health", "icon": "🧠"}
    ]
    return jsonify(actions)

if __name__ == "__main__":
    app.run(debug=True)