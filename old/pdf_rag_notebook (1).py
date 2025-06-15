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
from langchain_aws import ChatBedrock
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

def create_vector_store(chunks, embedding_model="amazon.titan-embed-text-v2:0"):
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

def setup_qa_chain(vectorstore, llm_model="amazon.nova-lite-v1:0", k=3):
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
    
    # Different models use different input formats
    # Chat models (like Claude 3, Llama 2 Chat) expect messages format
    # Text completion models (like Titan, older models) expect simple text
    
    chat_models = [
        "anthropic.claude-3-sonnet-20240229-v1:0",
        "anthropic.claude-3-haiku-20240307-v1:0", 
        "anthropic.claude-3-opus-20240229-v1:0",
        "meta.llama2-13b-chat-v1",
        "meta.llama2-70b-chat-v1"
    ]
    
    if llm_model in chat_models:
        # Use ChatBedrock for conversational models
        # These models expect structured conversation with roles
        print("📱 Using conversational model - ChatBedrock interface")
        llm = ChatBedrock(
            client=bedrock_client,
            model_id=llm_model,
            model_kwargs={
                "max_tokens": 1000,
                "temperature": 0.1,  # Low temperature for more focused answers
                "top_p": 0.9
            }
        )
    else:
        # Use regular Bedrock for text completion models
        # These models work with simple text input/output
        print("📝 Using text completion model - Bedrock interface")
        llm = Bedrock(
            client=bedrock_client,
            model_id=llm_model,
            model_kwargs={
                "max_tokens": 1000,
                "temperature": 0.1,
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
# STEP 6: Model Selection and Error Handling Guide
# =============================================================================

def get_available_models():
    """
    Helper function to understand different AWS Bedrock models and their capabilities.
    This educational function explains the differences between model types.
    """
    
    model_info = {
        "Chat Models (Conversational Interface)": {
            "anthropic.claude-3-opus-20240229-v1:0": "Most capable Claude model, best for complex reasoning",
            "anthropic.claude-3-sonnet-20240229-v1:0": "Balanced Claude model, good performance/cost ratio", 
            "anthropic.claude-3-haiku-20240307-v1:0": "Fastest Claude model, good for simple tasks",
            "meta.llama2-13b-chat-v1": "Open source conversational model, good general purpose",
            "meta.llama2-70b-chat-v1": "Larger Llama model, better reasoning capabilities"
        },
        
        "Text Completion Models (Simple Interface)": {
            "amazon.titan-text-express-v1": "AWS's own text model, cost-effective",
            "amazon.titan-text-lite-v1": "Lightweight version of Titan",
            "ai21.j2-mid-v1": "Jurassic-2 model, good for general text tasks",
            "ai21.j2-ultra-v1": "More capable Jurassic-2 model"
        }
    }
    
    print("🤖 Available AWS Bedrock Models for Q&A:")
    print("=" * 60)
    
    for category, models in model_info.items():
        print(f"\n📋 {category}:")
        for model_id, description in models.items():
            print(f"   • {model_id}")
            print(f"     └── {description}")
    
    print("\n💡 Recommendation: Start with 'anthropic.claude-3-haiku-20240307-v1:0' for testing")
    print("   (fastest and most cost-effective while still being very capable)")
    
    return model_info

def troubleshoot_common_errors():
    """
    Educational function that explains common errors and how to fix them.
    Understanding these patterns helps you become a better AI engineer.
    """
    
    print("🔧 Common Error Patterns and Solutions:")
    print("=" * 50)
    
    error_patterns = {
        "ValidationException: required key [messages] not found": {
            "cause": "Using wrong interface for chat models",
            "solution": "Use ChatBedrock instead of Bedrock for conversational models",
            "lesson": "Different model types expect different input formats"
        },
        
        "AccessDeniedException": {
            "cause": "Model not enabled in your AWS account",
            "solution": "Enable the model in AWS Bedrock console > Model access",
            "lesson": "Not all models are available by default - you need to request access"
        },
        
        "ThrottlingException": {
            "cause": "Making requests too quickly",
            "solution": "Add delays between requests or use exponential backoff",
            "lesson": "Rate limiting protects the service and ensures fair access"
        },
        
        "Invalid model identifier": {
            "cause": "Typo in model name or model not available in your region",
            "solution": "Check spelling and verify model availability in your AWS region",
            "lesson": "Model availability varies by region due to infrastructure constraints"
        }
    }
    
    for error, info in error_patterns.items():
        print(f"\n❌ Error: {error}")
        print(f"   🔍 Cause: {info['cause']}")
        print(f"   ✅ Solution: {info['solution']}")
        print(f"   📚 Learning: {info['lesson']}")

# =============================================================================
# STEP 7: Complete Example Usage with Error Handling
# =============================================================================

def main_demo(pdf_path="./your_document.pdf", model_id="anthropic.claude-3-haiku-20240307-v1:0"):
    """
    Complete demonstration of the PDF Q&A system with robust error handling.
    
    This function demonstrates the entire pipeline and teaches you to handle
    real-world issues that arise when building AI systems.
    
    Args:
        pdf_path: Path to your PDF file
        model_id: AWS Bedrock model to use for question answering
    """
    
    try:
        print("🚀 Starting PDF Q&A System Demo")
        print("=" * 50)
        
        # First, let's understand what models are available
        print("📚 Learning about available models...")
        get_available_models()
        print(f"\n🎯 Selected model: {model_id}")
        
        # Step 1: Load and process the PDF
        print(f"\n📄 Processing PDF document...")
        chunks = load_and_process_pdf(pdf_path)
        
        # Step 2: Create vector store with embeddings
        print(f"\n🧠 Creating embeddings and vector store...")
        vectorstore, embeddings = create_vector_store(chunks)
        
        # Step 3: Setup the QA chain with error handling
        print(f"\n🤖 Setting up question-answering system...")
        qa_chain = setup_qa_chain(vectorstore, llm_model=model_id)
        
        print("\n" + "=" * 50)
        print("🎉 System ready! You can now ask questions about your PDF.")
        print("=" * 50)
        
        # Example questions that work well with most documents
        example_questions = [
            "What is the main topic of this document?",
            "Can you provide a brief summary of the key points?",
            "What are the most important takeaways from this document?",
        ]
        
        # Demonstrate with example questions
        for question in example_questions:
            try:
                ask_question(qa_chain, question)
                print("\n" + "-" * 40)
            except Exception as e:
                print(f"❌ Error answering question '{question}': {str(e)}")
                print("💡 This might be a model-specific issue. Try a different model.")
        
        return qa_chain
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find PDF file at {pdf_path}")
        print("📝 Action needed: Please update the pdf_path parameter with the correct path to your PDF file.")
        print("💡 Example: main_demo('./documents/my_file.pdf')")
        return None
        
    except Exception as e:
        error_message = str(e)
        print(f"❌ Error: {error_message}")
        
        # Provide specific guidance based on the error type
        if "ValidationException" in error_message and "messages" in error_message:
            print("\n🔧 This looks like a model interface mismatch!")
            print("💡 Solution: The model you selected expects a different input format.")
            print("   Try using 'anthropic.claude-3-haiku-20240307-v1:0' instead.")
            print("   Or check the troubleshooting guide below:")
            troubleshoot_common_errors()
            
        elif "AccessDeniedException" in error_message:
            print("\n🔧 This looks like a model access issue!")
            print("💡 Solution: You need to enable this model in your AWS Bedrock console.")
            print("   1. Go to AWS Bedrock console")
            print("   2. Navigate to 'Model access'") 
            print("   3. Request access to the model you want to use")
            
        elif "credentials" in error_message.lower():
            print("\n🔧 This looks like an AWS credentials issue!")
            print("💡 Solution: Make sure your AWS credentials are configured.")
            print("   You can set them up using: aws configure")
            
        else:
            print("\n🔧 For help with this error, check the troubleshooting guide:")
            troubleshoot_common_errors()
        
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
# EXECUTION SECTION - How to Use This Notebook
# =============================================================================

# IMPORTANT: Update these paths and settings before running
YOUR_PDF_PATH = "relatorio_BTLG11.pdf"  # Change this to your PDF file path
RECOMMENDED_MODEL = "amazon.nova-lite-v1:0"  # Fast and reliable

print("📖 QUICK START GUIDE:")
print("=" * 50)
print("1. Update YOUR_PDF_PATH above with your actual PDF file path")
print("2. Make sure your AWS credentials are configured (aws configure)")
print("3. Run the main_demo function below")
print("4. If you get errors, check the troubleshooting guide")
print("")

# Run the complete demo with improved error handling
# This will walk you through the entire process step by step
####qa_system = main_demo(pdf_path=YOUR_PDF_PATH, model_id=RECOMMENDED_MODEL)

# Alternative models you can try if the default doesn't work:
# qa_system = main_demo(pdf_path=YOUR_PDF_PATH, model_id="anthropic.claude-3-sonnet-20240229-v1:0")
# qa_system = main_demo(pdf_path=YOUR_PDF_PATH, model_id="amazon.titan-text-express-v1")

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





qa_system = main_demo(pdf_path=YOUR_PDF_PATH, model_id=RECOMMENDED_MODEL)