import os  # for file handling
import glob  # for file handling
from typing import List  # for type hinting
from dotenv import load_dotenv  # for loading environment variables
from multiprocessing import Pool  # for parallel processing
from tqdm import tqdm  # for progress bar

from src.config import constants  # for loading settings
# for loading documents from various sources using langchain
from src.config import loader_mapping
from src.input.email_loader import EmailLoader  # for loading emails
# for splitting text into sentences
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma  # for storing vectors
from langchain.embeddings import HuggingFaceEmbeddings  # for generating embeddings
from langchain.docstore.document import Document  # for interacting with documents

load_dotenv()  # load environment variables from .env file

# get the directory to store the vectors
persist_directory = os.environ.get("PERSIST_DIRECTORY")
# get the directory to read the documents from
source_directory = os.environ.get("SOURCE_DIRECTORY","source_documents")
# get the name of the embedding model
embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
# get the chunk size for parallel processing
chunk_size = int(os.environ.get("CHUNK_SIZE"))
# get the chunk overlap for parallel processing
chunk_overlap = int(os.environ.get("CHUNK_OVERLAP"))


def does_vector_store_exist():
    """Check if the vector store already exists"""
    if os.path.exists(os.path.join(persist_directory, "index")):
        if (os.path.exists(os.path.join(persist_directory, "chroma-collections.parquet"))
                and os.path.exists(os.path.join(persist_directory, "chroma-embeddings.parquet"))):
            list_index_files = glob.glob(
                os.path.join(persist_directory, "index/*.bin"))
            list_index_files += glob.glob(
                os.path.join(persist_directory, "index/*.pkl"))

            # at least 3 documents are needed in a working vector store
            if len(list_index_files) > 3:
                return True
    return False


def load_single_document(file_path: str) -> Document:
    """Load a single document from a file path"""
    ext = "." + file_path.rsplit(".", 1)[-1]

    if ext in loader_mapping.LOADER_MAPPING:
        print("-------------ext----->", ext)
        loader_class, loader_args = loader_mapping.LOADER_MAPPING[ext]
        loader = loader_class(file_path, **loader_args)
        loader.load()


def load_documents(source_directory: str, ignored_files: List[str] = []) -> List[Document]:
    """Loads all documents from the source directory. Ignores files in ignored_files list"""
    all_files = []
    for ext in loader_mapping.LOADER_MAPPING:
        all_files.extend(
            glob.glob(os.path.join(source_directory, f"**/*{ext}"), recursive=True)
        )
    filtered_files = [file_path for file_path in all_files if file_path not in ignored_files]

    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(total=len(filtered_files), desc="Loading documents", ncols=80) as pbar:
            for i, docs in enumerate(pool.imap_unordered(load_single_document, filtered_files)):
                results.append(docs)
                pbar.update()

    return results


def process_documents(ignored_files: List[str] = []) -> List[Document]:
    """Load documents and split in chunks"""
    print(f"------------------------------->Loading documents from {source_directory}")
    documents = load_documents(source_directory, ignored_files)

    if not documents:
        print("------------------------------->No new documents to read")
        exit(0)

    print(f"------------------------------->Loaded {len(documents)} documents from {source_directory}")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    print(f"------------------------------->Split {len(texts)} chunks of text (max. {chunk_size} tokens each)")
    return texts


def ingest():
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

    if does_vector_store_exist():
        print(f"------------------------------->Appending to existing vector store at {persist_directory}")
        db = Chroma(persist_directory=persist_directory,
                    embedding_function=embeddings, client_settings=constants.CHROMA_SETTINGS)
        collection = db.get()
        texts = process_documents([metadata['source']
                                  for metadata in collection['metadatas']])
        print(f"------------------------------->Creating embeddings. May take a while...")
        db.add_documents(texts)
    else:
        print(f"------------------------------->Creating new vector store at {persist_directory}")
        texts = process_documents()
        print(f"------------------------------->Creating embeddings. May take a while...")
        db = Chroma(texts, embeddings, persist_directory=persist_directory,
                    client_settings=constants.CHROMA_SETTINGS)
    db.persist()
    db = None
    print("------------------------------->Ingestion complete. You Can run privateGPT.py to query your documents.")


def main():
    ingest()


if __name__ == "__main__":
    main()
