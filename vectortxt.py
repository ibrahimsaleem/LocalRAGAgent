from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os

txt_folder = "datatxt"  # Folder containing your txt files
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chrome_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    ids = []
    
    if os.path.exists(txt_folder):
        # List all .txt files in the folder
        txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]
        for file in txt_files:
            file_path = os.path.join(txt_folder, file)
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            # Remove extra whitespace and empty lines
            lines = [line.strip() for line in lines if line.strip()]
            chunk_size = 4  # Create chunks of 5 lines each
            
            chunks = [" ".join(lines[i:i+chunk_size]) for i in range(0, len(lines), chunk_size)]
            for idx, chunk in enumerate(chunks):
                doc_id = f"{os.path.splitext(file)[0]}_chunk_{idx+1}"
                document = Document(
                    page_content=chunk,
                    metadata={"source": file, "chunk": idx+1},
                    id=doc_id
                )
                ids.append(doc_id)
                documents.append(document)
    else:
        print(f"Folder '{txt_folder}' not found.")

vector_store = Chroma(
    collection_name="restaurant_reviews",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)
    
retriever = vector_store.as_retriever(
    search_kwargs={"k": 6}  # Adjust the number of retrieved documents as needed
)