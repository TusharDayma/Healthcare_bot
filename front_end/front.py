import streamlit as st
from src.rag_agent import ask
from datetime import datetime

def clean_response(text: str) -> str:
    """Clean response text for display."""
    if not text:
        return ""
    return text.replace('\n', '<br>').strip()

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "is_loading" not in st.session_state:
        st.session_state.is_loading = False

def display_chat_message(role: str, content: str, timestamp: str):
    """Display a chat message."""
    if role == "user":
        st.markdown(f"""
        <div style="margin: 10px; text-align: right;">
            <div style="background: #ffcc00; color: #1a1a1a; padding: 10px; border-radius: 15px; max-width: 70%; display: inline-block; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                {content}<br>
                <small style="color: #333;">{timestamp}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="margin: 10px; text-align: left;">
            <div style="background: #4CAF50; color: white; padding: 12px; border-radius: 15px; max-width: 70%; display: inline-block; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                <strong style="color: #ffffff;">Dr. HealthMate: </strong>{content}<br>
                <small style="color: #e0e0e0;">{timestamp}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_typing_indicator():
    """Display typing indicator."""
    st.markdown("""
    <div style="margin: 10px; text-align: left;">
        <div style="background: #4CAF50; color: white; padding: 12px; border-radius: 15px; display: inline-block; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <strong style="color: #ffffff;">Dr. HealthMate</strong> is typing...
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_timestamp():
    """Get current timestamp."""
    return datetime.now().strftime("%I:%M %p")

def main():
    # Page configuration
    st.set_page_config(
        page_title="Dr. HealthMate",
        page_icon="🩺",
        layout="wide"
    )

    # Updated CSS with beautiful design
    st.markdown("""
    <style>
        body {
            background-color: #1a1a1a;
            color: #ffffff;
            font-family: 'Arial', sans-serif;
        }
        .chat-container {
            background: #2c2c2c;
            padding: 20px;
            border-radius: 20px;
            max-height: 500px;
            overflow-y: auto;
            margin-bottom: 20px;
            border: 3px solid #4CAF50;
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }
        .stTextInput > div > div > input {
            background: #333;
            color: #fff;
            border: 2px solid #ffcc00;
            border-radius: 15px;
            padding: 12px;
            font-size: 16px;
        }
        .stButton > button {
            background: linear-gradient(45deg, #ffcc00, #ffaa00);
            color: #1a1a1a;
            border: none;
            border-radius: 15px;
            padding: 12px 25px;
            font-weight: bold;
            font-size: 16px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(255,204,0,0.4);
        }
        h1 {
            color: #4CAF50;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .stWarning {
            background-color: #333;
            border: 2px solid #ff4444;
            color: #ffcccc;
            padding: 15px;
            border-radius: 15px;
            font-size: 14px;
            box-shadow: 0 4px 8px rgba(255,68,68,0.2);
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    initialize_session_state()

    # Header
    st.header("🩺 Dr. HealthMate")

    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if st.session_state.messages:
        for message in st.session_state.messages:
            display_chat_message(message["role"], message["content"], message.get("timestamp"))
    else:
        st.write("Ask me about health-related questions!")
    
    if st.session_state.is_loading:
        display_typing_indicator()
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Input form
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your question...", placeholder="e.g., What are flu symptoms?")
        col_send, col_clear = st.columns([1, 1])
        
        with col_send:
            send_button = st.form_submit_button("Send")
        with col_clear:
            clear_button = st.form_submit_button("Clear Chat") if st.session_state.messages else None

    # Process messages
    if send_button and user_input.strip():
        timestamp = get_timestamp()
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": timestamp
        })
        st.session_state.is_loading = True
        st.rerun()

    if clear_button and st.session_state.messages:
        st.session_state.messages = []
        st.rerun()

    if st.session_state.is_loading:
        try:
            user_message = [msg for msg in st.session_state.messages if msg["role"] == "user"][-1]["content"]
            response = ask(user_message)
            cleaned_response = clean_response(response)
            formatted_response = (cleaned_response
                                .replace('<br>', '</p><p>')
                                .replace('1.', '<strong>1.</strong>')
                                .replace('2.,', '<strong>2.</strong>')
                                .replace('3.,', '<strong>3.</strong>')
                                .replace('4.,', '<strong>4.</strong>')
                                .replace('5.,', '<strong>5.</strong>')
                                .replace('association with', '<em>association with</em>')
                                .replace('should be used with caution', '<em>should be used with caution</em>')
                                .replace('is often recommended as a safer alternative', '<em>is often recommended as a safer alternative</em>')
                                .replace('can also be used to treat', '<em>can also be used to treat</em>'))
            st.session_state.messages.append({
                "role": "assistant",
                "content": formatted_response,
                "timestamp": get_timestamp()
            })
        except Exception:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Sorry, I encountered an error. Please try again.",
                "timestamp": get_timestamp()
            })
        finally:
            st.session_state.is_loading = False
            st.rerun()

    # Suggestions
    st.subheader("Quick Questions")
    suggestions = [
        "What are the symptoms of flu?",
        "How to manage diabetes?",
        "Benefits of regular exercise"
    ]
    for suggestion in suggestions:
        if st.button(suggestion):
            st.session_state.messages.append({
                "role": "user",
                "content": suggestion,
                "timestamp": get_timestamp()
            })
            st.session_state.is_loading = True
            st.rerun()

    # Disclaimer
    st.warning("This AI is for informational purposes only. Consult a healthcare professional for medical advice.")

if __name__ == "__main__":
    main()