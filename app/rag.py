import os
from dotenv import load_dotenv

# from langchain_openai import ChatOpenAI
# # from langchain.prompts import ChatPromptTemplate
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings    


load_dotenv()


class LocalRAG:
    def __init__(self):
        self.base_url = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
        self.api_key = os.getenv("LM_STUDIO_API_KEY", "lm-studio")
        self.model = os.getenv("LM_STUDIO_MODEL", "local-model")
        self.vectorstore_path = os.getenv("VECTOR_STORE_PATH", "vectorstore")
        self.pdf_path = os.getenv("PDF_PATH", "data/faq.pdf")

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.llm = ChatOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            model=self.model,
            temperature=0.2,
        )

        self.vectorstore = None
        self.retriever = None

    # def ingest_pdf(self):
    #     loader = PyPDFLoader(self.pdf_path)
    #     documents = loader.load()

    #     splitter = RecursiveCharacterTextSplitter(
    #         chunk_size=800,
    #         chunk_overlap=120
    #     )
    #     chunks = splitter.split_documents(documents)

    #     self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
    #     self.vectorstore.save_local(self.vectorstore_path)
    #     self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
    def ingest_pdf(self):
        loader = TextLoader(self.pdf_path, encoding="utf-8")
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=120
        )
        chunks = splitter.split_documents(documents)

        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        self.vectorstore.save_local(self.vectorstore_path)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
    def load_vectorstore(self):
        self.vectorstore = FAISS.load_local(
            self.vectorstore_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})

    def ensure_vectorstore(self):
        if os.path.exists(self.vectorstore_path):
            self.load_vectorstore()
        else:
            self.ingest_pdf()

    def ask(self, question: str) -> str:
        self.ensure_vectorstore()

        docs = self.retriever.invoke(question)
        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = ChatPromptTemplate.from_template(
            """
You are a customer support assistant.
Answer the user's question only using the provided context.
If the answer is not in the context, say that you could not find a reliable answer and suggest contacting support.

Context:
{context}

Question:
{question}
"""
        )

        chain = prompt | self.llm
        response = chain.invoke({
            "context": context,
            "question": question
        })

        return response.content