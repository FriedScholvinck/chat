import os
import time

from dotenv import load_dotenv
from llama_index import (Document, ServiceContext, StorageContext,
                         VectorStoreIndex, download_loader,
                         load_index_from_storage)

import openai
from llama_index.llms import OpenAI

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

LLM = True
URL = 'https://www.xomnia.com'
DEPTH = 2
name = URL.split('.')[-2].split('.')[-1]
DATA_DIR = f'data/{name}'

# check if there json files in data folder
if os.path.exists(f'{DATA_DIR}/docstore.json"'):

    # time function
    start = time.time()
    print("index already exists, loading...")
    # load index
    index_path = 'data'
    storage_context = StorageContext.from_defaults(persist_dir=DATA_DIR)
    index = load_index_from_storage(storage_context)
    print(index)
    # print time
    end = time.time()
    print(f"Loading index took {int(end - start)}s")

else:
    RemoteDepthReader = download_loader("RemoteDepthReader")

    loader = RemoteDepthReader(depth=DEPTH, domain_lock=True)
    documents = loader.load_data(url=URL)
    print(len(documents), 'documents loaded')

    service_context = None

    # create datadir of not exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt=f"You are an expert on the {name} website and your job is to answer technical questions. Assume that all questions are related to {name}. Keep your answers technical and based on facts – do not hallucinate features."))
    index = VectorStoreIndex.from_documents(documents, service_context=service_context, show_progress=True)
    index.storage_context.persist(DATA_DIR)

    