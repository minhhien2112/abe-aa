from typing import Union
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import  FileResponse
from fastapi_login.exceptions import InvalidCredentialsException
from setup import abe,get_object_frombyte,converObtobyte
import requests
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_GPP():
    x = requests.get('http://192.168.253.128:8000/GPP')
    a = get_object_frombyte(x.text)
    return a
path = "/home/ubuntu/code"
@app.get("/")
def read_root():
    return {"HelloAAAA": "WorldAAAAA"}

@app.post("/abe")
def handle(object: dict):
    print("OK")
    GPP = get_GPP()
    print(object)
    listaa = object['attribute']
    uname = object['uname']
    aa = object['aa']
    print(listaa)
    if (abe().checkattr(uname,listaa,aa) == False):
        return False
    return True

@app.get("/file")
def cat():
    file_path = os.path.join(path, "files/file.txt")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/plain", filename="Ciphertext.txt")
    return {"error" : "File not found!"}
