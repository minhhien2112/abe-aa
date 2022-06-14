from charm.toolbox.eccurve import prime192v1
import abenc_dacmacs_yj14
from charm.toolbox.pairinggroup import PairingGroup, GT,extract_key
import json
import requests
from charm.core.engine.util import objectToBytes,bytesToObject
import pickle
#import database
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction
import sys

groupObj = PairingGroup('SS512')
dac = abenc_dacmacs_yj14.DACMACS(groupObj)

def get_GPP():
    x = requests.get('http://192.168.253.128:8000/GPP')
    a = get_object_frombyte(x.text)
    return a
def get_object_frombyte(x):
	return bytesToObject(x.encode('ISO-8859-1'),groupObj)
def loadObject(filename):
	file = open(filename,"rb")
	x = pickle.load(file)
	y = bytesToObject(x, groupObj)
	file.close()
	return y
def writefilejs(ob,filename):
    file = open(filename,"w")
    file.write(json.dumps(ob,indent=10))
    file.close()
def encryptkeysearch(filename):
    GPP = get_GPP()
    file = open(filename,'r')
    authorities = loadObject("AuthorityAA.txt")
    data = json.load(file)
    policy = "(PROVIDER or PUBLICADMIN or TRANSACTIONSUPPORT or (CUSTOMER and VIP))"
    keys = data['data']
    res = {}
    res['id'] = data['id']
    k = groupObj.random(GT)
    print(k)
    a = SymmetricCryptoAbstraction(extract_key(k))
    ct = a.encrypt(keys)
    ct = objectToBytes(ct,groupObj).decode('ISO-8859-1')
    res['data'] = ct
    ct2 = dac.encrypt(GPP,policy,k,authorities['authorityM'])
    res['key'] = objectToBytes(ct2,groupObj).decode('ISO-8859-1')
    fname = "encrypted" + filename
    #print(res['key'])
    writefilejs(res,fname)
    return True
if __name__ == '__main__':
    encryptkeysearch('key-01.json')