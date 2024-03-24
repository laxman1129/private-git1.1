import os # for file handling
from dotenv import load_dotenv # for loading environment variables
from chromadb.config import Settings # for loading settings

load_dotenv() # load environment variables from .env file

PERSIST_DIRECTORY = os.environ.get("PERSIST_DIRECTORY") # get the directory to store the vectors

# define the Chroma settings
CHROMA_SETTINGS = Settings(
    chroma_db_impl='duckdb+parquet', # use the DuckDB implementation with Parquet files
    persist_directory=PERSIST_DIRECTORY, # store the vectors in the directory
    anonymized_telemetry=False, # do not send telemetry data
)