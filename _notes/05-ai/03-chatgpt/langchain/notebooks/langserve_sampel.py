#!/usr/bin/env python
import uvicorn #Uvicorn是一个快速的、基于异步的Python ASGI服务器，用于运行异步Web框架。它被广泛用于FastAPI和Starlette等现代Python Web框架中，以提供高性能和并发性。
from typing import List

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes

import os
from dotenv import load_dotenv, find_dotenv

from langchain_community.embeddings import QianfanEmbeddingsEndpoint
from langchain_community.chat_models import QianfanChatEndpoint
from langchain_openai import ChatOpenAI


def get_model(temperature=0.7):
    if current_llm == 'Qianfan':
        if temperature == 0:
            temperature = 0.01
        model = QianfanChatEndpoint(model="ERNIE-Bot-4", temperature = temperature)
    else:
        model = ChatOpenAI(model="gpt-4", temperature = temperature)
    return model
    
_ = load_dotenv(find_dotenv()) # read local .env file
current_llm = 'Qianfan'

server_name='15.15.174.4'
server_port = 8989  

# 1. Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# 2. Create model
model = get_model()

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser


# 4. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route

add_routes(
    app,
    chain,
    path="/chain",
)

uvicorn.run(app, host=server_name, port=server_port)