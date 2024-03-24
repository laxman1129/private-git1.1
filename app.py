#!/usr/bin/env python
import os
from src.input import ingest
from src.output import privateGPT
from dotenv import load_dotenv  # for loading environment variables

load_dotenv()

source_directory = os.environ.get("SOURCE_DIRECTORY","source_documents")

def main():
    print("------------------------------->Ingesting documents...")
    ingest.ingest()
    print("=======================================================")
    privateGPT.privateGPT()


if __name__ == "__main__":
    main()