from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
from src.config import CHROMA_PATH, EMBED_MODEL, LLM_MODEL

# Load vector store
embedding = OllamaEmbeddings(model=EMBED_MODEL)
vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)

# Retriever
retriever = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(),
    llm=ChatOllama(model=LLM_MODEL)
)

# Prompt
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are Dr. HealthMate, a highly experienced and professional medical doctor. You provide accurate, clear, and trustworthy medical advice based only on the verified medical literature provided in the context.

Your responsibilities include:
- Explaining diseases, symptoms, and medical terms in simple language
- Recommending over-the-counter medications when appropriate
- Providing first-aid tips and home remedies
- Advising when to consult a physician
- Never guessing — if the context does not contain a valid answer, respond with: "Based on the current information, I cannot provide a reliable answer. Please consult a qualified medical professional."

Only use the provided context to generate your response. Do NOT answer questions unrelated to medicine or healthcare.
"""),
    ("user", "Context:\n{context}\n\nQuestion: {question}")
])
# LLM
llm = ChatOllama(model=LLM_MODEL)

# Chain
qa_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | chat_prompt
    | llm
    | StrOutputParser()
)

def ask(question: str):
    return qa_chain.invoke(question)
