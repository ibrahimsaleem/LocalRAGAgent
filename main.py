# First, call the converter to process PDFs into txt
from convertors.txtconvertor import process_folder

input_folder = "data"
output_path = "datatxt/content.txt"
process_folder(input_folder, output_path)

import uuid
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from vectortxt import retriever, vector_store

model = OllamaLLM(model="deepseek-r1:8b")

template = """
You are an expert in answering questions about a pizza restaurant

Here are some relevant data: {reviews}

Here is the question to answer based on above data: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

query_count = 0   # Counter for queries

while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break

    reviews = retriever.invoke(question)
    # Print out the reviews that are sent in the prompt
    print("------ Retrieved Reviews ------")
    print(reviews)
    print("------ End of Reviews ------")

    result = chain.invoke({"reviews": reviews, "question": question})
    print(result)

    # Create a new document containing the question, answer, and context
    conversation_text = f"Question: {question}\nAnswer: {result}\nContext: {reviews}"
    conv_doc = Document(
        page_content=conversation_text,
        metadata={"source": "conversation"}
    )
    conv_doc_id = "conv_" + str(uuid.uuid4())
    
    # Add the conversation document to the vector store for future retrieval (RAG)
    vector_store.add_documents(documents=[conv_doc], ids=[conv_doc_id])
    
    query_count += 1
    # Cleanup conversation documents every 10 queries
    if query_count % 10 == 0:
        print("Cleaning up conversation documents from vector store...")
        # Delete conversation docs using a metadata filter (syntax may depend on your vector store API)
        vector_store.delete_documents(filter={"metadata.source": "conversation"})
        print("Cleanup complete.")