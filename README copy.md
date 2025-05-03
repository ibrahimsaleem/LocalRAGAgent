# LocalAIAgentWithRAG

LocalAIAgentWithRAG is a Retrieval-Augmented Generation (RAG) system that allows you to convert PDF or plain text files into a vector database, and then use that context to answer user queries using an LLM (via Ollama). The agent extracts data from PDFs, saves the text output, splits the text into meaningful chunks, and indexes them using the Chroma vector store. When a query is asked, the system retrieves relevant documents and supplies them as context to the LLM to generate an answer.

## Features

- **PDF and Text Input:**  
  Extract text from PDF files using the provided converter, or use pre-existing text files.  
- **Chunking and Vectorization:**  
  Splits text into fixed-sized chunks and converts them into embeddings stored in a Chroma vector database.  
- **Retrieval-Based Querying:**  
  Retrieves relevant chunks from the vector database based on query similarity.  
- **LLM Integration via Ollama:**  
  Uses an Ollama LLM (e.g., `deepseek-r1:8b` or any other available model) to generate answers based on the retrieved context.
- **Conversation History (RAG):**  
  Optionally stores past Q&A interactions in the vector store to enrich future queries.

## Code Structure

- **`main.py`**  
  The main entry point for the application. It first calls the PDF-to-text converter, then loads the vector database, retrieves context for a user's query, and finally uses the LLM to generate an answer. It also adds the conversation (query, answer, and context) to the vector store for future retrieval.

- **`convertors/txtconvertor.py`**  
  Contains code to extract text from PDF files and save the result as a text file. This is used before vectorizing the content.

- **`vectortxt.py`**  
  Processes text files located in the `datatxt` folder. It splits each file into chunks (customizable chunk size, e.g., 2, 4, or 5 lines per chunk), converts them into embeddings, and stores them in the Chroma vector database. Retrieval settings (number of documents to retrieve) are also configured here.

- **`requirements.txt`**  
  Lists the dependencies required to run the project. The pared-down version includes LangChain, Chroma, Ollama, and PDF conversion tools.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/LocalAIAgentWithRAG.git
   cd LocalAIAgentWithRAG
   ```

2. **Set Up a Virtual Environment:**

   On Windows:
   ```bash
   python -m venv agentenv
   agentenv\Scripts\activate
   ```

   On macOS/Linux:
   ```bash
   python3 -m venv agentenv
   source agentenv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure Ollama and the Desired LLM are Installed:**  
   Use the `ollama list` command to verify the available models and make sure the model referenced in `main.py` (e.g., `deepseek-r1:8b`) is available.

## Usage

1. **Prepare Your Data:**  
   - Place your PDF files in the `data` folder.
   - Alternatively, place your text files in the `datatxt` folder if you want to skip PDF conversion.

2. **Run the Application:**

   ```bash
   python main.py
   ```

   The application will:
   - Extract text from PDFs and save it to a text file.
   - Process text files to build the vector database.
   - Prompt you for questions.
   - Retrieve context from indexed documents.
   - Generate answers using the LLM and display the results.

3. **Query Conversation:**  
   As you ask questions, the system displays the retrieved reviews and generated answers. Conversation history is stored to allow quicker retrieval for similar future queries. Every 10 queries, conversation documents are cleaned up from the vector store.

## Customization

- **Chunk Size and Retrieval Count:**  
  In `vectortxt.py`, you can adjust:
  
  - `chunk_size`: Number of lines per chunk (e.g., 2, 4, 5, etc.).
  
  - In `retriever = vector_store.as_retriever(search_kwargs={"k": 6})`, you can change the number of documents to retrieve (e.g., set to 10).

- **LLM Model:**  
  Change the model in `main.py` by updating:
  
  ```python
  model = OllamaLLM(model="deepseek-r1:8b")
  ```
  to your preferred model (available via `ollama list`).

## Troubleshooting

- **Model Not Found:**  
  If you encounter errors like "model not found", ensure your model name exactly matches one from the `ollama list` output.

- **PDF Conversion Issues:**  
  If PDF extraction fails, ensure the necessary dependencies (such as `pdf2image` and `PyPDF2`) are properly installed.

## License

This project is provided under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements

- [LangChain](https://github.com/hwchase17/langchain) for the framework.
- [Chroma](https://github.com/chroma-core/chromadb) for the vector storage solution.
- [Ollama](https://ollama.ai) for providing the interface to LLMs.

Enjoy using LocalAIAgentWithRAG and feel free to contribute or share feedback!