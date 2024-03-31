from langchain.vectorstores.redis import Redis
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
from langchain_community.llms import HuggingFaceEndpoint
from langchain.document_loaders import DataFrameLoader

from langchain_community.document_loaders import PyPDFLoader
from langchain.vectorstores.redis import Redis
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import logging

# import xmltodict, json
from utils.ccd_parse import HL7Parser

import pandas as pd
import sys
sys.path.append('../')

from constants import (
    SERVER_URL,
    LLM_URL,
    INDEX,
    REDIS_URL,
    HF_KEY
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

huggingface_ef = HuggingFaceInferenceAPIEmbeddings(
    api_key=HF_KEY, model_name="sentence-transformers/all-MiniLM-l6-v2"
)

def ingest_data(data, huggingface_ef, index_):
    logger.info(f"ingest_data index: {index_}")
    rds = Redis.from_texts(
        data,
        huggingface_ef,
        redis_url=REDIS_URL,
        index_name=index_,
    )    
    return rds

def get_text_chunks_langchain(python_documents):
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=400, chunk_overlap=5
    )
    docs = [x.page_content for x in python_splitter.split_documents(python_documents)]
    return docs

def get_text_chunks(python_documents):
    python_splitter = RecursiveCharacterTextSplitter.from_language(
      language=Language.PYTHON, chunk_size=800, chunk_overlap=0
    )
    docs = [x.page_content for x in python_splitter.split_documents(python_documents)]
    return docs

def dropIndex(index_):
    Redis.drop_index(index_name=f"{index_}", delete_documents=True, redis_url=REDIS_URL)
    
def process_pdf(file_input):
    dropIndex("ml_pdf")
    loader = PyPDFLoader(file_input.name)
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=400, chunk_overlap=5
    )
    
    data = loader.load_and_split(python_splitter)
    for i in range(1, len(data),3):
        chunks = get_text_chunks_langchain(data[i:i+3])

        print("chunks =>", chunks, "\n\n")
        print("type of chunk", type(chunks), "\n\n")
        
        rds = ingest_data(chunks, huggingface_ef, "ml_pdf")
    logger.info("ingestion done!")
    return rds

def process_xml(file_input):
    logger.info("XML processing started")
    dropIndex(INDEX)
    hl7_parser = HL7Parser(file_input.name)
    data = hl7_parser.details
    if data:
        dataFrame = pd.DataFrame.from_records([data])
        dataFrame['text'] = dataFrame.apply(lambda x: ', '.join([f"{col}:{val}" for col, val in x.items()]),axis=1)
        loader = DataFrameLoader(dataFrame)
        data = loader.load()
        chunks = get_text_chunks(data)
        rds = ingest_data(chunks, huggingface_ef, INDEX)
    data = hl7_parser.aut_details
    if data:
        dataFrame = pd.DataFrame.from_records([data])
        dataFrame['text'] = dataFrame.apply(lambda x: ', '.join([f"{col}:{val}" for col, val in x.items()]), axis=1)
        loader = DataFrameLoader(dataFrame)
        data = loader.load()
        chunks = get_text_chunks(data)
        rds = ingest_data(chunks, huggingface_ef, INDEX)
    data = hl7_parser.data_enterer_details
    if data:
        dataFrame = pd.DataFrame.from_records([data])
        dataFrame['text'] = dataFrame.apply(lambda x: ' '.join(x),axis=1)
        loader = DataFrameLoader(dataFrame)
        data = loader.load()
        chunks = get_text_chunks(data)
        rds = ingest_data(chunks, huggingface_ef, INDEX)
    informant_details = hl7_parser.informant_details
    if informant_details:
        for informant in informant_details:
            dataFrame = pd.DataFrame.from_records([informant])
            dataFrame['text'] = dataFrame.apply(lambda x: ' '.join(x),axis=1)
            loader = DataFrameLoader(dataFrame)
            data = loader.load()
            chunks = get_text_chunks(data)
            rds = ingest_data(chunks, huggingface_ef,INDEX)
        
    component_details = hl7_parser.component_details
    if component_details:
        dataFrame = pd.DataFrame.from_records([component_details])
        dataFrame['text'] = dataFrame.apply(lambda x:', '.join([f"{col}:{val} " for col, val in x.items()]), axis=1)
        loader = DataFrameLoader(dataFrame)
        data = loader.load()
        chunks = get_text_chunks(data)
        if len(chunks) > 10 :
            for i in range(0, len(chunks),10):
                chunk = chunks[i:i+10]
                rds = ingest_data(chunk, huggingface_ef, INDEX)
        else :        
            rds = ingest_data(chunks, huggingface_ef, INDEX)
    logger.info("CCD file uploaded successfully.")
    return rds



def get_tgi_llm(): 
    from langchain_community.llms import HuggingFaceTextGenInference
    
    # llm = HuggingFaceTextGenInference(
    #     inference_server_url=LLM_URL,
    #     max_new_tokens=1024,
    #     top_k=10,
    #     top_p=0.95,
    #     typical_p=0.95,
    #     temperature=0.01,
    #     repetition_penalty=1.03,
    #     streaming=False,
    #     server_kwargs={
    #         "headers": {
    #             "Authorization": f"Bearer {HF_KEY}",
    #             "Content-Type": "application/json",
    #         }
    #     },
    # )
    
    llm = HuggingFaceEndpoint(
        repo_id=LLM_URL, temperature=0.01, huggingfacehub_api_token=HF_KEY
    )
    
    logger.info("Language model loaded.")
    return llm