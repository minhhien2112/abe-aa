import requests
from typing import Union
import json
from setup import abe,get_object_frombyte
from fastapi import FastAPI
def get_GPP():
    x = requests.get('http://192.168.253.128:8000/GPP')
    a = get_object_frombyte(x.text)
    return a
def get_GMK():
    x = requests.get('http://192.168.253.128:8000/GMK')
    a = get_object_frombyte(x.text)
    print(a)
    return a
def handleRequestUser(uname,listattr):
    GPP = get_GPP()
    if (abe.checkattr(uname,listattr) == False):
        print("Input Attribute Incorrect")
        return
    print("Input Attribute is valid")
    key = value().getukey(uname)
    ct = value().getciphertext(GPP,"Document1",key)
    for i in ct:
        print(i)
        print(json.dumps(ct[i], indent = 10 ))
def run():
    listatt = ["REALESTATE", "FINANCE"]  
    handleRequestUser("lily", listatt)
#    print(get_key("lily"))
if __name__ == '__main__':
    run()