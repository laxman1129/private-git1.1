#!/usr/bin/env python
import os
os.environ['HTTP_PROXY'] = 'http://zscaler.emirates.com:10068'
os.environ['HTTPS_PROXY'] = 'http://zscaler.emirates.com:10068'

from src.input.ingest import ingest
from src.output.privateGPT import privateGPT

def main():
    print("Ingesting documents...")
    ingest()
    print("Ingestion complete. You Can run privateGPT.py to query your documents.")


if __name__ == "__main__":
    main()