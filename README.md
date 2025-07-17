# 🩺 Healthcare AI Agent (LangChain + Ollama + ChromaDB)

A local Retrieval-Augmented Generation (RAG) chatbot designed to answer medical questions using the **Gale Encyclopedia of Medicine** as its knowledge base. This project leverages cutting-edge AI technologies to provide accurate and context-aware responses for healthcare-related queries.

## 📖 Project Overview

The Healthcare AI Agent is a locally deployable chatbot that combines LangChain, Ollama, and ChromaDB to create a robust RAG system. It uses the `llama3.2` model for natural language processing and `nomic-embed-text` for embeddings, with ChromaDB as the vector store for efficient retrieval of relevant medical information.

## 🧠 Tech Stack

- LangChain: Framework for building applications with LLMs and external data.
- Ollama: Local LLM inference with `llama3.2` for generation and `nomic-embed-text` for embeddings.
- ChromaDB: Vector database for storing and retrieving medical knowledge embeddings.
- Python: Version 3.10 or higher.

## 🚀 Usage

### Prerequisites
Before setting up the project, ensure you have the following installed:
- Python 3.10 or higher
- pip (Python package manager)
- Git (for cloning the repository)
- Ollama installed locally (follow instructions at [Ollama's official site](https://ollama.ai/))
- Access to the Gale Encyclopedia of Medicine dataset (ensure it is properly formatted and accessible)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Ollama:
   - Ensure the `llama3.2` and `nomic-embed-text` models are pulled:
     ```bash
     ollama pull llama3.2
     ollama pull nomic-embed-text
     ```

4. Configure ChromaDB:
   - Initialize the ChromaDB vector store and load the Gale Encyclopedia of Medicine dataset (refer to the project’s `data/` directory or documentation for specific instructions).

5. Run the chatbot:
   ```bash
   python main.py
   ```

### Example
Once the chatbot is running, you can interact with it via the command line or a provided interface. Example query:
```
What are the symptoms of diabetes?
```
The chatbot will retrieve relevant information from the Gale Encyclopedia of Medicine and generate a response using the `llama3.2` model.

## 📂 Project Structure
```
├── data/                  # Directory for the Gale Encyclopedia dataset
├── src/                   # Source code for the chatbot
├── requirements.txt       # Python dependencies
├── main.py                # Entry point for running the chatbot
└── README.md              # Project documentation
```

## 🛠️ Development Setup

To contribute to the project or customize the chatbot:
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies as described above.
3. Modify the code in the `src/` directory or update the dataset in `data/`.
4. Test changes locally before committing.

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes and commit them (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature-name`).
5. Open a pull request with a clear description of your changes.

Please ensure your code follows PEP 8 guidelines and includes appropriate documentation.

## ⚠️ Notes
- This project is intended for educational and research purposes. Always consult a qualified medical professional for real-world medical advice.
- Ensure the Gale Encyclopedia of Medicine dataset is legally obtained and properly licensed for use.
- Performance may vary based on hardware, especially for running Ollama locally.

## 📬 Contact
For questions or feedback, please open an issue on GitHub or contact [your-email@example.com].

## 📝 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Changes Made
1. Enhanced Structure: Added sections like Project Overview, Prerequisites, Installation, Project Structure, Development Setup, Contributing, Notes, Contact, and License to make the README more comprehensive and professional.
2. Clearer Instructions: Expanded the Usage section with detailed steps for cloning, setting up Ollama, and running the chatbot. Included commands for creating a virtual environment.
3. Professional Tone: Polished the language to make it more engaging and aligned with typical GitHub README standards.
4. Maintained Core Content: Kept the original tech stack, usage instructions, and purpose intact while enhancing clarity and adding context.
5. Added Best Practices: Included sections for contributing, licensing, and project structure to make the repository more contributor-friendly and complete.
6. Safety Note: Added a disclaimer about consulting medical professionals and ensuring legal use of the dataset.

### Suggestions for Further Improvement
- Add a Demo: If possible, include a GIF or screenshot of the chatbot in action to make the README visually appealing.
- Specify Dataset Format: Provide details on how the Gale Encyclopedia of Medicine dataset should be formatted or where to obtain it (if publicly available).
- Include Troubleshooting: Add a section for common issues (e.g., Ollama setup errors, ChromaDB connection problems) and their solutions.
- Link to Documentation: If your project has additional documentation (e.g., in a `docs/` folder), link to it.
- Badges: Add GitHub badges for build status, license, or Python version to enhance credibility.
