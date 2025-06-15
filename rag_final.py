# Cell 1: Install required packages
#pip install langchain langchain-community langchain-aws pypdf faiss-cpu tiktoken
# Cell 2: Import necessary libraries
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings, ChatBedrock
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
# Cell 3: Configure AWS credentials (if not already configured)
# Make sure you have AWS credentials configured either through:
# - AWS CLI: aws configure
# - Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
# - IAM role (if running on AWS infrastructure)

# Optional: Set region if needed
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"  # Change to your preferred region
# Cell 4: Initialize embedding model
embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v2:0",
    region_name="us-east-1"  # Change to your region
)
# Cell 5: Load and process PDF
# Specify your PDF file path
pdf_path = "./documentos_pdf/relatorio_BTLG11.pdf"  # Change this to your PDF file path

# Load PDF
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

chunks = text_splitter.split_documents(documents)
print(f"Number of chunks created: {len(chunks)}")
# Cell 6: Create vector store
# Create FAISS vector store from documents
vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)

print("Vector store created successfully!")
# Cell 7: Initialize LLM
llm = ChatBedrock(
    model_id="amazon.nova-lite-v1:0",
    model_kwargs={
        "temperature": 0.1,
        "max_tokens": 5120
    },
    region_name="us-east-1"  # Change to your region
)
# Cell 8: Create custom prompt template
prompt_template = """Use the following context to answer the question at the end. 
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.
Always cite the relevant parts of the context in your answer. Answer in Portuguese.

Context: {context}

Question: {question}

Answer:"""

PROMPT = PromptTemplate(
    template=prompt_template, 
    input_variables=["context", "question"]
)
# Cell 9: Create RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}  # Return top 4 most similar chunks
    ),
    chain_type_kwargs={"prompt": PROMPT},
    return_source_documents=True
)
# Cell 10: Function to ask questions
def ask_question(question):
    """
    Ask a question about the PDF content
    """
    result = qa_chain.invoke({"query": question})
    
    print(f"Question: {question}")
    print(f"\nAnswer: {result['result']}")
    print("\n" + "="*50 + "\n")
    
    # Optionally print source documents
    if result.get('source_documents'):
        print("Source chunks used:")
        for i, doc in enumerate(result['source_documents']):
            print(f"\nChunk {i+1}:")
            print(f"Page: {doc.metadata.get('page', 'N/A')}")
            print(f"Content: {doc.page_content[:200]}...")
            print("-"*30)
    
    return result
# Cell 11: Example usage - Ask questions about your PDF
# Example questions (modify based on your PDF content)
questions = [
    "What is the main topic of this document?",
    "Can you summarize the key points?",
    "What are the main conclusions?"
]

for question in questions:
    result = ask_question(question)
    print("\n" + "="*70 + "\n")
# Cell 12: Interactive Q&A session
# Interactive loop for asking questions
print("PDF Q&A System Ready!")
print("Type 'quit' to exit")
print("-" * 50)

while True:
    user_question = input("\nEnter your question: ")
    
    if user_question.lower() in ['quit', 'exit', 'q']:
        print("Exiting Q&A session...")
        break
    
    if user_question.strip():
        ask_question(user_question)
# Cell 13: Optional - Save and load vector store
# Save vector store to disk for later use
vectorstore.save_local("pdf_vectorstore")

# To load it later:
# loaded_vectorstore = FAISS.load_local(
#     "pdf_vectorstore", 
#     embeddings,
#     allow_dangerous_deserialization=True
# )