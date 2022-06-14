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
def decryptkeysearch(filename,fileattr):
    GPP = get_GPP()
    file = open(filename,'r')
    attributekey = loadObject(sys.argv[1])
    data = json.load(file)
    k = get_object_frombyte(data['key'])
    TK = dac.generateTK(GPP, k, attributekey['authoritySecretKeys'], attributekey['keys'][0])
    key = dac.decrypt(k, TK, attributekey['keys'][1])
    print(key)
    a = SymmetricCryptoAbstraction(extract_key(key))
    res = data.copy()
    del res['key']
    ob = get_object_frombyte(res['data'])
    s = a.decrypt(ob)
    s = s.decode('ISO-8859-1')
    res['data'] = s
    fname = "decrypted" + filename
    writefilejs(res,fname)
    return True
if __name__ == '__main__':
    decryptkeysearch('encryptedkey-01.json',sys.argv[1])