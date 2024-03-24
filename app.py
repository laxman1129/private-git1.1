#!/usr/bin/env python
import glob
import os
from src.input import ingest
from src.config import loader_mapping
from dotenv import load_dotenv  # for loading environment variables

load_dotenv()

source_directory = os.environ.get("SOURCE_DIRECTORY","source_documents")

def main():
    print("------------------------------->Ingesting documents...")
    ingest.ingest()

    print("------------------------------->Ingestion complete. You Can run privateGPT.py to query your documents.")


if __name__ == "__main__":
    main()