# PDF Document Q&A System using AWS Bedrock and LangChain
# This notebook demonstrates how to build a Retrieval Augmented Generation (RAG) system
# that can answer questions about PDF documents using AWS services

# First, let's install and import all necessary libraries
# Run this cell first to ensure all dependencies are available

import os
import boto3
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# LangChain imports for document processing and RAG pipeline
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

print("✅ All imports successful!")

# =============================================================================
# STEP 1: AWS Configuration and Setup
# =============================================================================

# Configure AWS credentials and region
# Make sure you have AWS credentials configured either through:
# 1. AWS CLI (aws configure)
# 2. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
# 3. IAM roles (if running on EC2)

AWS_REGION = "us-east-1"  # Change this to your preferred region
os.environ["AWS_DEFAULT_REGION"] = AWS_REGION

# Initialize AWS Bedrock client
# Bedrock is AWS's managed service for foundation models
bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name=AWS_REGION
)

print(f"✅ AWS Bedrock client configured for region: {AWS_REGION}")

# =============================================================================
# STEP 2: Document Loading and Preprocessing
# =============================================================================

def load_and_process_pdf(pdf_path, chunk_size=1000, chunk_overlap=200):
    """
    Load a PDF file and split it into manageable chunks for processing.
    
    Why we split documents:
    - Large documents can exceed model context limits
    - Smaller chunks provide more focused retrieval
    - Overlapping chunks ensure important information isn't lost at boundaries
    
    Args:
        pdf_path: Path to the PDF file
        chunk_size: Maximum characters per chunk
        chunk_overlap: Number of characters to overlap between chunks
    """
    
    # Check if PDF file exists
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    print(f"📄 Loading PDF from: {pdf_path}")
    
    # Load the PDF using PyPDFLoader
    # This extracts text content while preserving document structure
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    print(f"📊 Loaded {len(documents)} pages from PDF")
    
    # Split documents into chunks for better processing
    # RecursiveCharacterTextSplitter tries to keep related content together
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]  # Split on paragraphs first, then sentences
    )
    
    # Split all documents into chunks
    chunks = text_splitter.split_documents(documents)
    
    print(f"✂️  Split into {len(chunks)} text chunks")
    print(f"📏 Average chunk size: {sum(len(chunk.page_content) for chunk in chunks) // len(chunks)} characters")
    
    return chunks

# =============================================================================
# STEP 3: Embedding Generation and Vector Store Creation
# =============================================================================

def create_vector_store(chunks, embedding_model="amazon.titan-embed-text-v1"):
    """
    Convert text chunks into vector embeddings and store them in a searchable format.
    
    Embeddings are numerical representations of text that capture semantic meaning.
    Similar texts will have similar vector representations, enabling semantic search.
    
    Args:
        chunks: List of document chunks to embed
        embedding_model: AWS Bedrock embedding model to use
    """
    
    print(f"🧠 Creating embeddings using model: {embedding_model}")
    
    # Initialize Bedrock embeddings
    # This connects to AWS Bedrock's embedding models
    embeddings = BedrockEmbeddings(
        client=bedrock_client,
        model_id=embedding_model
    )
    
    # Create FAISS vector store from document chunks
    # FAISS (Facebook AI Similarity Search) enables fast similarity search
    # It runs entirely in memory for this example
    print("🔄 Generating embeddings and building vector index...")
    
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    
    print("✅ Vector store created successfully!")
    print(f"📊 Indexed {len(chunks)} document chunks")
    
    return vectorstore, embeddings

# =============================================================================
# STEP 4: Question Answering Setup
# =============================================================================

def setup_qa_chain(vectorstore, llm_model="anthropic.claude-3-sonnet-20240229-v1:0", k=3):
    """
    Create a question-answering chain that uses retrieved context to answer questions.
    
    This implements Retrieval Augmented Generation (RAG):
    1. Retrieve relevant chunks based on question similarity
    2. Use retrieved context to generate accurate answers
    
    Args:
        vectorstore: The vector store containing document embeddings
        llm_model: AWS Bedrock model for question answering
        k: Number of relevant chunks to retrieve for each question
    """
    
    print(f"🤖 Setting up QA chain with model: {llm_model}")
    
    # Initialize Bedrock LLM
    llm = Bedrock(
        client=bedrock_client,
        model_id=llm_model,
        model_kwargs={
            "max_tokens": 1000,
            "temperature": 0.1,  # Low temperature for more focused answers
            "top_p": 0.9
        }
    )
    
    # Create a custom prompt template for better answers
    # This helps the model understand its role and how to use the context
    prompt_template = """
    You are a helpful AI assistant that answers questions based on the provided context from a document.
    
    Use the following context to answer the question at the end. If you don't know the answer based on the context, just say that you don't know - don't make up an answer.
    
    Context:
    {context}
    
    Question: {question}
    
    Answer: Let me help you with that based on the document content.
    """
    
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    # Create the QA chain
    # This combines retrieval with generation for accurate answers
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # "stuff" means put all retrieved docs into prompt
        retriever=vectorstore.as_retriever(search_kwargs={"k": k}),
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True  # This lets us see which chunks were used
    )
    
    print("✅ QA chain setup complete!")
    return qa_chain

# =============================================================================
# STEP 5: Main Execution Function
# =============================================================================

def ask_question(qa_chain, question):
    """
    Ask a question and get an answer with source information.
    
    Args:
        qa_chain: The configured QA chain
        question: The question to ask about the document
    """
    
    print(f"\n❓ Question: {question}")
    print("🔍 Searching for relevant information...")
    
    # Get answer from the QA chain
    result = qa_chain({"query": question})
    
    answer = result["result"]
    source_docs = result["source_documents"]
    
    print(f"\n💡 Answer: {answer}")
    
    # Show which parts of the document were used to answer
    print(f"\n📚 Based on {len(source_docs)} relevant sections:")
    for i, doc in enumerate(source_docs, 1):
        # Show first 150 characters of each source chunk
        preview = doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
        print(f"   {i}. {preview}")
        if hasattr(doc, 'metadata') and 'page' in doc.metadata:
            print(f"      (Page {doc.metadata['page'] + 1})")
    
    return answer, source_docs

# =============================================================================
# STEP 6: Complete Example Usage
# =============================================================================

def main_demo():
    """
    Complete demonstration of the PDF Q&A system.
    This ties together all the components we've built.
    """
    
    # Path to your PDF file - update this to your actual file path
    PDF_PATH = "./your_document.pdf"  # Change this to your PDF file path
    
    try:
        print("🚀 Starting PDF Q&A System Demo")
        print("=" * 50)
        
        # Step 1: Load and process the PDF
        chunks = load_and_process_pdf(PDF_PATH)
        
        # Step 2: Create vector store with embeddings
        vectorstore, embeddings = create_vector_store(chunks)
        
        # Step 3: Setup the QA chain
        qa_chain = setup_qa_chain(vectorstore)
        
        print("\n" + "=" * 50)
        print("🎉 System ready! You can now ask questions about your PDF.")
        print("=" * 50)
        
        # Example questions - customize these based on your document
        example_questions = [
            "What is the main topic of this document?",
            "Can you summarize the key points?",
            "What are the important dates mentioned?",
        ]
        
        # Demonstrate with example questions
        for question in example_questions:
            ask_question(qa_chain, question)
            print("\n" + "-" * 40)
        
        return qa_chain
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find PDF file at {PDF_PATH}")
        print("Please update the PDF_PATH variable with the correct path to your PDF file.")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

# =============================================================================
# STEP 7: Interactive Question Function
# =============================================================================

def interactive_qa(qa_chain):
    """
    Interactive function to ask custom questions about your PDF.
    Call this after running main_demo() to ask your own questions.
    """
    
    if qa_chain is None:
        print("❌ QA chain not initialized. Please run main_demo() first.")
        return
    
    print("\n🎯 Interactive Q&A Mode")
    print("Ask questions about your PDF document. Type 'quit' to exit.")
    print("-" * 50)
    
    while True:
        question = input("\n❓ Your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not question:
            continue
            
        ask_question(qa_chain, question)

# =============================================================================
# EXECUTION SECTION
# =============================================================================

# Run the complete demo
# Make sure to update PDF_PATH in main_demo() function before running
qa_system = main_demo()

# Uncomment the line below to start interactive mode after the demo
# interactive_qa(qa_system)

# =============================================================================
# ADDITIONAL UTILITY FUNCTIONS
# =============================================================================

def test_similarity_search(vectorstore, query, k=5):
    """
    Test the similarity search functionality to see what chunks are retrieved.
    This helps debug and understand how well your embeddings work.
    """
    
    print(f"🔍 Testing similarity search for: '{query}'")
    docs = vectorstore.similarity_search(query, k=k)
    
    print(f"📊 Found {len(docs)} similar chunks:")
    for i, doc in enumerate(docs, 1):
        preview = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
        print(f"\n{i}. {preview}")
        if hasattr(doc, 'metadata'):
            print(f"   Metadata: {doc.metadata}")

def save_vector_store(vectorstore, save_path="./vector_store"):
    """
    Save the vector store to disk for future use.
    This avoids re-processing the same PDF multiple times.
    """
    
    vectorstore.save_local(save_path)
    print(f"💾 Vector store saved to: {save_path}")

def load_vector_store(embeddings, load_path="./vector_store"):
    """
    Load a previously saved vector store from disk.
    """
    
    vectorstore = FAISS.load_local(load_path, embeddings)
    print(f"📂 Vector store loaded from: {load_path}")
    return vectorstore

print("\n" + "=" * 60)
print("📖 INSTRUCTIONS:")
print("1. Update PDF_PATH in main_demo() function with your PDF file path")
print("2. Ensure your AWS credentials are configured")
print("3. Run main_demo() to start the system")
print("4. Use interactive_qa() for custom questions")
print("=" * 60)