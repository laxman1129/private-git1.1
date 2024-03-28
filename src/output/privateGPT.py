#!/usr/bin/env python
import os
import time
import argparse
from dotenv import load_dotenv

from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp

from src.config import constants

import gradio as gr

load_dotenv()

embeddings_model_name = os.environ.get('EMBEDDINGS_MODEL_NAME')
persist_directory = os.environ.get('PERSIST_DIRECTORY')

model_type = os.environ.get('MODEL_TYPE')

vicuna_model_path = os.environ.get('VICUNA_MODEL_PATH')
vicuna_model_n_ctx= os.environ.get('VICUNA_MODEL_N_CTX')

gpt_model_path = os.environ.get('GPT_MODEL_PATH')
gpt_model_n_ctx= os.environ.get('GPT_MODEL_N_CTX')

model_n_batch = int(os.environ.get('MODEL_N_BATCH'))
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS', 4))


def parse_arguments():
    parser = argparse.ArgumentParser(description='Private GPT : Ask questions to your dowcuments without internet connection,'
                                     ' using a locally hosted LLMs.')
    parser.add_argument('--hide-source', "-S", action='store_true',
                        help='Hide the source document in the output')
    parser.add_argument("--mute-stream", "-M", action='store_true',
                        help='Mute the output stream callback from LLM')

    return parser.parse_args()

def llm_function(question, chat_history):
    args = parse_arguments()
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    db = Chroma(persist_directory=persist_directory,
                embedding_function=embeddings, client_settings=constants.CHROMA_SETTINGS)
    retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
    callback = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]

    match model_type:
        case "GPT4All":
            llm = GPT4All(model_path=gpt_model_path,
                          n_ctx=gpt_model_n_ctx,
                          backend='gptj',
                          n_batch=model_n_batch,
                          callbacks=callback,
                          verbose=False)
        case "LlamaCpp":
            llm = LlamaCpp(model_path=vicuna_model_path,
                           n_ctx=vicuna_model_n_ctx,
                           n_batch=model_n_batch,
                           callbacks=callback,
                           verbose=False)
        case _:
            raise ValueError(f"Unknown model type: {model_type}")

    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=not args.hide_source)
    res = qa(question)
    answer = res['result']
    return answer
    
    

def privateGPT():    
    title = "Incident IQ"
    examples = [
        "Why did CDS fail",
        "Why did not receive meal allowance"
    ]

    gr.ChatInterface(
        fn= llm_function,
        title=title,
        examples=examples
    ).launch()


    # while True:
    #     question = input("\nAsk a question: ")
    #     if question.lower() in ['exit', 'quit']:
    #         break
    #     if question.strip() == "":
    #         continue

    #     start = time.time()
    #     res = qa(question)
    #     answer, docs = res['result'], [
    #     ] if args.hide_source else res['source_documents']
    #     end = time.time()

    #     print(f"Question: {question}")
    #     print(f"Answer: {answer}")
    #     print(f"Time taken: {end - start:.2f}s")


    #     for doc in docs:
    #         print(f"\n> " + doc.metadata['source'] + ":")
    #         print(doc.page_content)
