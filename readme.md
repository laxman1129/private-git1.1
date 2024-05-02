# Private GPT

## What is private GPT

## How to build and run the project

### building the project
- create conda environment and activate it
    - https://llama-cpp-python.readthedocs.io/en/latest/install/macos/
    
    ```
    conda create -p venv python --y
    conda info --envs
    conda activate <venv> 
    ```
- install the requirements, it takes some time (7-10 minutes)
    ```
    pip install -r requirements.txt
    ```
- download model from huggingface
    ```
    https://huggingface.co/vicuna/ggml-vicuna-13b-1.1/tree/main
    ```

## System Requirements

## Flow

- `ingest.py`
    
    - This script processes the documents stored in the `source_docs` folder
    - while processing the document, this script loads only the new documents in the folder
    - langchain `document loaders` are used to load the files based on their extentions
    - landchain `text splitter` is used to recursively split the text to chunk size and overlap
    - these texts are then stored in the vector db using the `huggingface embeddings`
    - this process converts the documents to embeddings which the langchain models understands
    -


## Terminologies

- `Embedding`  
    An embedding is a numerical representation of a piece of information, for example, text, documents, images, audio, etc. The representation captures the semantic meaning of what is being embedded

## Reasonings

- Why use `all-MiniLM-L6-v2` embedding models ?
    `https://www.sbert.net/docs/pretrained_models.html`  
    As per above link, `all-MiniLM-L6-v2` is 5 times faster but still provides good quality.
    We can use other other models as per our requirements.



---

## References

- https://ts.llamaindex.ai/

---
## models

ggml-gpt4all-j-v1.3-groovy.bin  
ggml-vic13b-q5_1.bin  
ggml-vic13b-uncensored-q5_1.bin  
ggml-vic13b-uncensored-q8_0.bin

---
## fixing 

```
pip install certifi
python -m certifi
ln -s /opt/anaconda3/envs/privategpt/lib/python3.12/site-packages/certifi/cacert.pem cert.pem
rehash
```

https://stackoverflow.com/a/75111104

https://discuss.huggingface.co/t/using-huggingface-embeddings-completely-locally/70837


download manually : https://www.kaggle.com/datasets/shinomoriaoshi/sentencetransformersallminilml6v2?resource=download

https://github.com/UKPLab/sentence-transformers/issues/1462


curl --insecure -O https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/distilbert-base-nli-stsb-mean-tokens.zip

unzip distilbert-base-nli-stsb-mean-tokens.zip -d ./sent_bert


pip install –trusted-host pypi.org \
–trusted-host huggingface.co \
