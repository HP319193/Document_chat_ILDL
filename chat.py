import gradio as gr
from langchain.vectorstores.redis import Redis
from langchain.chains import RetrievalQA as chain
from utils.gen_prompts import Prompts
from utils.styles import button_css , header, seaTheam
import logging
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from constants import (
    format_prompt
)

from utils.utility import get_tgi_llm
from utils.utility import process_pdf
from utils.utility import process_xml

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
k = 5
system_prompt = ""
prompt = ""
rds = None

app = FastAPI(title="Doc UI")
# Allow all origins (not recommended for production)
origins = ["*"]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/health")
def health():
    return "ok"

llm = get_tgi_llm()

def loading_pdf():
    return "Loading..."

# def upload_file(filepath):
#     return filepath

def add_text(history, text):
    history = history + [(text, None)]
    return history, ""


def create_index(file_input):
    logger.info("File upload process started:")
    global rds

    if file_input is not None:
        audio_file_name = file_input.split("/")[-1]
        logger.info(f"File upload process started:{audio_file_name}")
        
        try:
            file_ext = audio_file_name.split(".")[1]
            if "pdf" in  file_ext:
               rds = process_pdf(file_input)
               return f"{audio_file_name} 📊 processed successfully "
            elif "xml" == file_ext:
               rds = process_xml(file_input)
               return f"{audio_file_name} 🌐 processed successfully "
            else:
                logger.error(f"Format not support:{audio_file_name}")
                raise ValueError('Format not support')  
            #
        finally:
            logger.info(f"File upload process completed:{audio_file_name}")

def chat(question, chat_history, sys_prompt, tokens):
    global system_prompt
    global k
    global rds

    if re.search(Prompts.DEMOGRAPHIC.name, question, re.IGNORECASE):
        system_prompt = Prompts.DEMOGRAPHIC.value
        prompt = format_prompt(
        system_prompt= system_prompt, user_prompt=question)
    elif re.search(question,Prompts.Encounter.name, re.IGNORECASE):
        system_prompt = Prompts.DEFAULT.value  + Prompts.Encounter.value    
    elif re.search("Reason for Visit", question, re.IGNORECASE):
        system_prompt = Prompts.DEFAULT.value  + Prompts.Encounter.value    
    elif re.search(question, Prompts.LabResults.name ,  re.IGNORECASE):
        system_prompt = Prompts.DEFAULT.value + Prompts.LabResults.value    
    elif re.search(question,Prompts.Medications.name,  re.IGNORECASE):
        system_prompt = Prompts.DEFAULT.value + Prompts.Medications.value 
    elif re.search(question, Prompts.Smoking.name,  re.IGNORECASE):
        system_prompt = Prompts.DEFAULT.value + Prompts.Smoking.value      
    elif re.search(question, Prompts.SDoH.name, re.IGNORECASE):
        system_prompt = Prompts.DEFAULT.value + Prompts.SDoH.value  
    elif re.search(Prompts.Summarize.name, question, re.IGNORECASE):
        system_prompt = Prompts.DEFAULT.value + Prompts.Summarize.value           
    elif re.search(Prompts.PROBLEM.name, question, re.IGNORECASE):
        system_prompt = Prompts.DEFAULT.value + Prompts.PROBLEM.value
    elif re.search(Prompts.diabetes.name, question, re.IGNORECASE):
        system_prompt = Prompts.DEFAULT.value + Prompts.diabetes.value    
    elif re.search("Medical condition", question, re.IGNORECASE):
        system_prompt = Prompts.DEFAULT.value + Prompts.MED_CONDITION.value                              
    else:
        system_prompt = Prompts.DEFAULT.value

    prompt = format_prompt(user_prompt=question,
        system_prompt= system_prompt )
    retriever = rds.as_retriever(
        search_type="similarity_score_threshold", search_kwargs={"k": k,"score_threshold": 0.1}
    )
    qa = chain.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True
    )
    
    bot_response = qa(prompt)
    response = bot_response['result']
    yield response

with gr.Blocks(css=button_css, title="Chat App",
               analytics_enabled=False,
               head="CCD- chat box",
               theme=seaTheam) as demo:
    
    chatbot = gr.Chatbot(height=800,render=False, elem_id="chatbot")
    demo.dev_mode = False
    with gr.Row(elem_id="header-wrapper"):
        with gr.Column(elem_id="logo"):
             gr.Image(value='./utils/chat-bot-logo.png', width=10,show_label=False,show_download_button=False, elem_id="logo-img")
        with gr.Column(elem_id="logo-title"):
             gr.HTML(header)   
    with gr.Row(variant="panel"):
        with gr.Column('button-inline'):
            pdf_doc = gr.File(label="Load a CCD file", file_types=['.xml','.pdf'], type="filepath", min_width=100, height=100) 
            load_pdf = gr.Button("📁Upload",  variant='primary')
            langchain_status = gr.Textbox(label="File upload status", placeholder="...", interactive=False, container=True, scale=7, render=True,max_lines=1)
            clearBtn = gr.ClearButton(value="Clear", elem_id="cancel-button", elem_classes="cancel-button") 
            
        with gr.Column(scale=8):    
            interface = gr.ChatInterface(
                chat, 
                chatbot=chatbot,
                analytics_enabled=False,
                cache_examples=False,
                textbox=gr.Textbox(label="Question", placeholder="Type your question and hit Enter ", container=False, scale=7, render=False), 
            )  

        load_pdf.click(create_index, inputs=[pdf_doc], outputs=[langchain_status], queue=False)
        clearBtn.click(lambda: None, None, langchain_status, queue=False)
        clearBtn.click(lambda: None, None, pdf_doc, queue=False)
   
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=6000)

