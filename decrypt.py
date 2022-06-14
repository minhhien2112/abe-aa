import abenc_dacmacs_yj14
from charm.toolbox.eccurve import prime192v1
import abenc_dacmacs_yj14
import json
import sys
import pickle
import requests
from charm.core.engine.util import objectToBytes,bytesToObject
from charm.toolbox.pairinggroup import PairingGroup, GT,extract_key
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction

groupObj = PairingGroup('SS512')
dac = abenc_dacmacs_yj14.DACMACS(groupObj)
def decrypt(GPP,data,attributekey):
    if (isinstance(data, str)):
        return data
    k = get_object_frombyte(data['key'])
    TK = dac.generateTK(GPP, k, attributekey['authoritySecretKeys'], attributekey['keys'][0])
    key = dac.decrypt(k, TK, attributekey['keys'][1])
    res = data.copy()
    del res['key']
    if (key == False):
        res = dict.fromkeys(res, "*** NO PERMISSION ***")
        return res
    a = SymmetricCryptoAbstraction(extract_key(key))
    for i in res:
        ob = get_object_frombyte(res[i])
        s = a.decrypt(ob)
        try:
            s = bytesToObject(s,groupObj)
        except:
            s = s.decode('UTF-8')
        # if (isinstance(s.decode('UTF-8'),str)):
        #     s = s.decode('UTF-8')
        # else:
        res[i] = s
    return res
def get_object_frombyte(x):
	return bytesToObject(x.encode('UTF-8'),groupObj)
def getvalueptfile(filename):
    path = "data/" + filename
    file = open(path,"r")
    data = json.load(file)
    file.close()
    return data
def get_GPP():
    x = requests.get('http://192.168.253.128:8000/GPP')
    a = get_object_frombyte(x.text)
    return a
def loadObject(filename):
	file = open(filename,"rb")
	x = pickle.load(file)
	y = bytesToObject(x, groupObj)
	file.close()
	return y
khanh = loadObject(sys.argv[2])
attributekey = khanh
GPP = get_GPP()
i = sys.argv[1]
filename = "encrypted/" + "encrypted" + "document" + str(i) + ".json"
data = getvalueptfile(filename)
ab = data['Provider']
for k in ab:
    if (k == 'Management and construction information'):
        for j in ab[k]:
            data['Provider'][k][j] = decrypt(GPP,data['Provider'][k][j],attributekey)
        continue
    data['Provider'][k] = decrypt(GPP,data['Provider'][k],attributekey)
for k in data:
    if (k == 'Provider') or (k == 'id'):
        continue
    for j in data[k]:
        data[k][j] = decrypt(GPP,data[k][j],attributekey)
print(json.dumps(data,indent=10))
