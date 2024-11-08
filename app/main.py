from llama_index.core import Document
from llama_index.core import VectorStoreIndex, DocumentSummaryIndex
from llama_index.core.node_parser import SentenceSplitter
from langchain_ollama import OllamaLLM
from llama_index.core import Settings
from langchain.llms import BaseLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import pathlib
from translator import Translator
from file_parser import File_parser
import os
import warnings

# The line BaseLLM.predict = patched_predict overrides the deprecated predict method and uses invoke instead.
# This should ensure that anywhere the predict method is called within llama_index, it uses invoke
def patched_predict(self, prompt, **kwargs):
    return self.invoke(prompt, **kwargs)


# load a specific prompt from a given file
def load_prompt(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


# Define the input/output files
current_dir = os.path.dirname(__file__)
resource_dir = os.path.join(current_dir, '..', 'resource')
outputs_dir = os.path.join(current_dir, '..', 'outputs')

input_file_path = os.path.join(resource_dir,'Soilanalysis-38-Zannias','108','240438-zannias-kephales-bio.pdf')
response_file = os.path.join(outputs_dir, 'SOIL_ANALYSIS_RES.txt')
text_output_file = os.path.join(outputs_dir, 'SOIL_ANALYSIS_TEXT.txt')


if __name__ == "__main__":
    translator = Translator()
    file_parser = File_parser()
    warnings.filterwarnings("ignore")

    # Load the prompt
    prompt = load_prompt(os.path.join(resource_dir, 'prompt.txt'))

    BaseLLM.predict = patched_predict

    # Extract text from file
    file_text = file_parser.extract_text_from_file(input_file=input_file_path)

    # Translate the text if needed
    translated_text = translator.text_translator(file_text)

    # Store the text in a file
    #pathlib.Path(text_output_file).write_bytes(translated_text.encode())
    with open(text_output_file, "w", encoding='utf-8') as file:
        file.write(translated_text)


    # Create the documents
    documents = [Document(text=translated_text)]
    
    # Load the model 
    llm = OllamaLLM(model="llama3.1:8b", temperature = 0.1)

    # Load the embedding Model
    embed_model = HuggingFaceEmbedding('paraphrase-multilingual-MiniLM-L12-v2')

    # The Settings class in llama_index (formerly known as GPT Index) is used to configure
    # global parameters that influence how the library interacts with language models (LLMs),
    # embedding models, and other system components.
    Settings.llm = llm
    Settings.embed_model = embed_model
    Settings.context_window = 2048

    # Specify the splitter
    splitter = SentenceSplitter(chunk_size=700)

    # Create the query engine
    document_summary_index = DocumentSummaryIndex.from_documents(documents,splitter=splitter)
    query_engine_summary_index = document_summary_index.as_query_engine()
   
    # Create the response
    response = query_engine_summary_index.query(prompt)
    
    # Create a json Response
    json_response = file_parser.create_json(response=response)

    # Write the respose to a file
    with open(response_file, "w", encoding='utf-8') as file:
        file.write(str(json_response))