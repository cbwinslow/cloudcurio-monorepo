from typing import List, Dict, Any
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
import os

class RAGSystem:
    """Retrieval-Augmented Generation system for enhanced AI responses"""
    
    def __init__(self):
        """Initialize the RAG system with vector store and LLM"""
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.llm = OpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7
        )
        
        # Initialize vector store
        self.vector_store = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def add_documents(self, documents: List[str], metadata: List[Dict] = None):
        """Add documents to the vector store"""
        # Create Document objects
        docs = []
        for i, text in enumerate(documents):
            doc_metadata = metadata[i] if metadata and i < len(metadata) else {}
            docs.append(Document(page_content=text, metadata=doc_metadata))
        
        # Split documents into chunks
        split_docs = self.text_splitter.split_documents(docs)
        
        # Add to vector store
        self.vector_store.add_documents(split_docs)
        self.vector_store.persist()
    
    def query(self, question: str, k: int = 4) -> str:
        """Query the vector store and generate response"""
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": k})
        )
        
        # Generate response
        response = qa_chain.invoke(question)
        return response["result"]
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Perform similarity search on the vector store"""
        return self.vector_store.similarity_search(query, k=k)

# Global RAG system instance
rag_system = RAGSystem()