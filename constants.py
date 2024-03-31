import os
from dotenv import load_dotenv
load_dotenv()
SERVER_URL = os.getenv("EMBED_SERVER_URL") 
REDIS_URL = os.getenv("REDIS_SERVER_URL") 
LLM_URL = os.getenv("LLM_URL") 
INDEX = os.getenv("INDEX_NAME")
HF_KEY = os.getenv("HF_KEY")


base_prompt = "<s>[INST]\n<<SYS>>\n{system_prompt}\n<</SYS>>\n\n{user_prompt}[/INST]"

def format_prompt(user_prompt, system_prompt=""):
    if system_prompt.strip():
        return f"<s>[INST]\n<<SYS>>\n{system_prompt}\n<</SYS>>\n\n{user_prompt}[/INST]"
    return f"<s>[INST]{user_prompt}[/INST]"

CONTEXT_WINDOW_SIZE = 2048
MAX_NEW_TOKENS = 700 # int(CONTEXT_WINDOW_SIZE/4)
N_GPU_LAYERS = 83 
N_BATCH = 512
separators = ["\n\n", "\n", " "]