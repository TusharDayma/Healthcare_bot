from src.rag_agent import ask

if __name__ == "__main__":
    print("🤖 Healthcare Agent Ready. Type 'exit' to quit.")
    while True:
        user_input = input("👤 You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = ask(user_input)
        print("🤖 Bot:", response)
