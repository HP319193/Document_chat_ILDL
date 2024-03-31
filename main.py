from langchain_community.llms import HuggingFaceEndpoint    
llm = HuggingFaceEndpoint(
    repo_id="BAAI/bge-large-en-v1.5", temperature=0.01, huggingfacehub_api_token="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")

# from langchain_community.llms import HuggingFaceTextGenInference

# ENDPOINT_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
# HF_TOKEN = "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"

# llm = HuggingFaceTextGenInference(
#     inference_server_url=ENDPOINT_URL,
#     max_new_tokens=210,
#     # top_k=50,
#     # temperature=0.1,
#     # repetition_penalty=1.03,
#     server_kwargs={
#         "headers": {
#             "Authorization": f"Bearer {HF_TOKEN}",
#             "Content-Type": "application/json",
#         }
#     },
# )

llm("What did foo say about bar?")

# import requests
# API_URL = "https://api-inference.huggingface.co/models/gpt2"
# headers = {"Authorization": f"Bearer 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"}
# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()
# data = query("Can you please let us know more details about your ")

# print(data)