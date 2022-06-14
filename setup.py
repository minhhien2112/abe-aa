from charm.toolbox.eccurve import prime192v1
import abenc_dacmacs_yj14
from charm.toolbox.pairinggroup import PairingGroup, GT,extract_key
import json
import requests
from charm.core.engine.util import objectToBytes,bytesToObject
import pickle
from json import JSONEncoder 
#import database
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction
from itertools import chain
import sys
index_list = ["Seller detail", "Buyer detail", "Property Detail", "Purchase price", "Time and payments", "Construction detail"]
except_list =["Addition Services","Time", "Payments", "Construction costs"]

groupObj = PairingGroup('SS512')
dac = abenc_dacmacs_yj14.DACMACS(groupObj)
H = lambda x: groupObj.hash(x, G1)

def writefile(ob, filename):
	file = open(filename,"wb")
	object_byte = objectToBytes(ob, groupObj)
	pickle.dump(object_byte,file)
	file.close()
def writefilejs(ob,filename):
    file = open(filename,"w")
    file.write(json.dumps(ob,indent=10))
    file.close()
def prepare():
	GMK = {}
	GPP, GMK = dac.setup1()
	print("GMK =",GMK)
	print("GPP = ", GPP)
	writefile(GPP,"GPP.txt")
	writefile(GMK,"GPP.txt")
	print("=======Load Data=======")
def loadGPP():
	file = open("GPP.txt","rb")
	GPP = pickle.load(file)
	GMK = pickle.load(file)
	file.close()
	return GPP,GMK
def loadObject(filename):
	file = open(filename,"rb")
	x = pickle.load(file)
	y = bytesToObject(x, groupObj)
	file.close()
	return y
def addUser(GPP,name, filename, attrlist, users, aa1):
    u = { 'id': name, 'authoritySecretKeys': {}, 'keys': None}
    u['keys'], users[u['id']] = dac.registerUser(GPP)
    for attr in attrlist:
        dac.keygen(GPP, aa1, attr, users[u['id']], u['authoritySecretKeys'])
    writefile(u,filename)
def get_key(id,k):
	t = database.get_key(id,k).encode('UTF-8')
	key = bytesToObject(t, groupObj)
	return key
def get_object_frombyte(x):
	return bytesToObject(x.encode('UTF-8'),groupObj)
def converObtobyte(x):
	return objectToBytes(x,groupObj).decode('UTF-8')
def symeencrypt_value(id , index):
	key = get_key(id,index)
	z = database.get_value(id,index)
	a = SymmetricCryptoAbstraction(extract_key(key))
	print("index", index)
	print(json.dumps(z, indent=10))
	if (index == "Construction detail"):
		del z["Payments"]
	for i in z:
		if (isinstance(z[i], str)):
			msg = z[i].encode('UTF-8')
		else:
			msg = objectToBytes(z[i],groupObj)
		ct = a.encrypt(msg)
		ct = objectToBytes(ct,groupObj).decode('UTF-8')
		database.uploaddbct(id,index, i, ct)
	return
def symeencrypt_value1(data):
    if (isinstance(data, str)):
        return
    key = get_object_frombyte(data['key'])
    doc = data.copy()
    del doc['key']
    a = SymmetricCryptoAbstraction(extract_key(key))
    for i in doc:
        if (isinstance(doc[i], str)):
            msg = doc[i].encode('UTF-8')
        else:
            msg = objectToBytes(doc[i],groupObj)
        ct = a.encrypt(msg)
        ct = objectToBytes(ct,groupObj).decode('UTF-8')
        data[i] = ct
def encrypted_keywpc(GPP,authority,data,d, listitem):
    if (isinstance(data, str)):
        return False
    policy = listitem[d]
    key = get_object_frombyte(data['key'])
    ct = dac.encrypt(GPP,policy,key,authority)
    data['key'] = objectToBytes(ct,groupObj).decode('UTF-8')
    return True
def decrypt_documentbyuseraatrkey(GPP, u,id):
	print("Using {} Secrert key ".format(u['id']))
	for i in index_list:
		decrypt_value(GPP, id, u, i)
def encrypt_key_uploaddbct(GPP, id,listpolicy, aa1):
	listitem = {index_list[i]: listpolicy[i] for i in range(len(index_list))}
#	print(json.dumps(listitem, indent=6))
	for i in listitem:
		add_key_toDbCT(GPP, id, i, listitem[i], aa1)
def encrypt_value_uploaddb(id):
	for i in index_list:
		symeencrypt_value(id , i)
def genkey_adddbpt(id, key_list1):
	for i in key_list1:
		k = groupObj.random(GT)
		tmp = objectToBytes(k, groupObj)
		database.add_key_value(id,i,tmp.decode('UTF-8'))
def setup_genkeyaddpt(id):
	for i in index_list:
		k = groupObj.random(GT)
		print(k)
		tmp = objectToBytes(k, groupObj)
		print(tmp.decode('UTF-8'))
		database.add_key_value(id,i,tmp.decode('UTF-8'))
	#=======For payments==============
def gen_addkey_symeencryptforpaym(GPP, id, policy,aa1):
	#=======Genkey upload to DBPT=======
	k = groupObj.random(GT)
	database.upload_keypaym(1,id,objectToBytes(k,groupObj).decode('UTF-8'))
	#====Getkey and upload to DBCT=======
	key = database.get_keypm(1,id)
	k = get_object_frombyte(key)
	print("k", k)
	CT = dac.encrypt(GPP, policy, k, aa1)
	tmp = objectToBytes(CT,groupObj)
	database.upload_keypaym(2, id,tmp.decode('UTF-8'))
	#====================================
	#========Syme Encrypt value===========
	z = database.get_value_pm(1,id)
	key = database.get_keypm(1,id)
	key = get_object_frombyte(key)
	a = SymmetricCryptoAbstraction(extract_key(key))
	for i in z:
		msg = z[i].encode('UTF-8')
		ct = a.encrypt(msg)
		ct = objectToBytes(ct,groupObj).decode('UTF-8')
		database.upload_value_pmct(id,i,ct)
	return
def add_key_toDbCT(GPP, id, index, policy, aa1):
	key = get_key(id,index)
	CT = dac.encrypt(GPP, policy, key, aa1)
	tmp = objectToBytes(CT,groupObj)
	database.uploaddbct(id, index, "key", tmp.decode('UTF-8'))
	return
def decrypt_value_pm(GPP,id, attributekey):
	z = database.get_value_pm(2,id)
	k = database.get_keypm(2,id)
	k = get_object_frombyte(k)
	TK = dac.generateTK(GPP, k, attributekey['authoritySecretKeys'], attributekey['keys'][0])
	key = dac.decrypt(k, TK, attributekey['keys'][1])
	if (key == False):
		z = dict.fromkeys(z, "*** NO PERMISSION ***")
		return z
	a = SymmetricCryptoAbstraction(extract_key(key))
	for i in z:
		ob = get_object_frombyte(z[i])
		s = a.decrypt(ob)
		z[i] = s.decode('UTF-8')
	return z

def decrypt_value(GPP, id, attributekey, index):
	z = database.get_valuect(id, index)
	k = database.get_keyct(id,index)
	k = get_object_frombyte(k)
	TK = dac.generateTK(GPP, k, attributekey['authoritySecretKeys'], attributekey['keys'][0])
	key = dac.decrypt(k, TK, attributekey['keys'][1])
	print(index)
	if (key == False):
		z = dict.fromkeys(z, "*** NO PERMISSION ***")
		print(json.dumps(z, indent=10))
		return
	a = SymmetricCryptoAbstraction(extract_key(key))
	if (index == "Construction detail"):
		del z["Payments"]
	for i in z:
		ob = get_object_frombyte(z[i])
		s = a.decrypt(ob)
		if (i in except_list):
#			print(i)
			s = bytesToObject(s,groupObj)
#			print(type(s))
			z[i] = s
			continue
		z[i] = s.decode('UTF-8')
	if (index == "Construction detail"):
		z["Payments"] = decrypt_value_pm(GPP,id, attributekey)
	print(json.dumps(z, indent=10))
	return
def setup_final(GPP, listpolicy, policy7 , aa1, id):
	setup_genkeyaddpt(id)
	database.create_sampledbct(id)
	encrypt_key_uploaddbct(GPP, id,listpolicy, aa1)
	encrypt_value_uploaddb(id)
	gen_addkey_symeencryptforpaym(GPP, id, policy7,aa1)
def getvalueptfile(filename):
    path = "data/" + filename
    file = open(path,"r")
    data = json.load(file)
    file.close()
    return data
def getvaluectfile(filename):
    path = "data/" + filename
    file = open(path,"r")
    data = json.load(file)
    file.close()
    return data
def addkeytodict(data):
    for i in data:
        k = groupObj.random(GT)
        tmp = objectToBytes(k, groupObj).decode('UTF-8')
        data[i]['key'] = tmp
def addkeytodict2(data,index):
    k = groupObj.random(GT)
    tmp = objectToBytes(k, groupObj).decode('UTF-8')
    if isinstance(data, str):
        t = {}
        t[index] = data
        print(index)
        t['key'] = tmp
        print(t)
        data = t
        print(data)
    data['key'] = tmp

def get_GPP():
    x = requests.get('http://192.168.253.128:8000/GPP')
    a = get_object_frombyte(x.text)
    return a
class abe():
    def __init__(self):
        file = open("userattr.json","r")
        self.dictattr = json.load(file)
    def checkattr(self,uname: str, listattr, aa):
        for i in self.dictattr[aa]:
            if i['user_name'] == uname.upper():

                for attr in listattr:
                    if  attr not in i['attribute']:
                        print(attr)
                        return False
        return True
def encryptkeysearch(GPP,filename,authority):
    file = open(filename,'r')
    data = json.load(file)
    policy = "(PROVIDER or PUBLICADMIN or TRANSACTIONSUPPORT or (CUSTOMER and VIP))"
    keys = data['data']
    res = {}
    res['id'] = data['id']
    k = groupObj.random(GT)
    a = SymmetricCryptoAbstraction(extract_key(k))
    ct = a.encrypt(keys)
    ct = objectToBytes(ct,groupObj).decode('UTF-8')
    res['data'] = ct
    ct2 = dac.encrypt(GPP,policy,k,authority)
    res['key'] = objectToBytes(ct2,groupObj).decode('UTF-8')
    fname = "encrypted" + filename
    #print(res['key'])
    writefilejs(res,fname)
    return True
def run():
    print("==============Run Program===========")
    GPP = get_GPP()
    users = {}
    authorities = {}
    authorityAttributes1 =  ["OWNERPROJECT","INVESTOR","BUSINESSMANAGER","SALESSPECIALIST",\
    "SALEAGENT", "DESIGNER","MANAGER","STAFF","CONSTRUCTION","SUPERVISION", "PROVIDER"]
    authorityAttributes2 = ["PUBLICADMIN","DIRECTOR","ADMINISTRATIVESTAFF","RECEIPTSTAFF"]
    authorityAttributes3 = ["TRANSACTIONSUPPORT","SALEAGENTS","CREDITAPPROVALOFFICER","MANAGER","CUSTOMER","NORMAL","VIP"]
    authorityAttributesM = []
    authorityAttributesM = authorityAttributes1 + authorityAttributes2 + authorityAttributes3
    NamAttribute = ["PROVIDER","OWNERPROJECT","INVESTOR"]
    KhanhAttribute = ["PROVIDER","OWNERPROJECT","SALESSPECIALIST"]
#======================Setup Authority And Write to file ===========================
    authority1 = "authority1"
#     dac.setupAuthority1(GPP, authority1, authorityAttributes1, authorities)
# #    writefile(authorities[authority1],"Authority1.txt")

    authority2 = "authority2"
#     dac.setupAuthority1(GPP, authority2, authorityAttributes2, authorities)
# #    writefile(authorities[authority2],"Authority2.txt")

    authority3 = "authority3"
    authorityM = "authorityM"
#     dac.setupAuthority1(GPP, authority3, authorityAttributes3, authorities)
# #    writefile(authorities[authority3],"Authority3.txt")
#     writefile(authorities,"AuthorityAA.txt")
    # dac.setupAuthority1(GPP, authorityM, authorityAttributesM, authorities)
    # writefile(authorities,"AuthorityAA.txt")
    
    authorities = loadObject("AuthorityAA.txt")

    encryptkeysearch(GPP,"key-01.json",authorities[authorityM])
    # aa1 = loadObject("Authority1.txt")
    # aa2 = loadObject("Authority2.txt")
    # aa3 = loadObject("Authority3.txt")
    # print(aa1)
    # print(aa2)
    # print(aa3)    
#=============================Create User and write to file =======================
#======================Alice Bob========
    # khanh = { 'id': 'khanh', 'authoritySecretKeys': {}, 'keys': None}
    # khanh['keys'], users[khanh['id']] = dac.registerUser(GPP)
    # for attr in KhanhAttribute:
    #     dac.keygen(GPP, authorities[authorityM], attr, users[khanh['id']], khanh['authoritySecretKeys'])
    # writefile(khanh,"Khanhke,y.txt")


    #addUser(GPP,'khanh','Khanhkey.txt', ['PROVIDER','OWNERPROJECT','SALESSPECIALIST'], users, authorities[authorityM])
    # addUser(GPP,'mai','Maikey.txt', ["PUBLICADMIN","DIRECTOR"], users, authorities[authorityM])
    # addUser(GPP,'nam','Namkey.txt', ["PROVIDER","OWNERPROJECT","INVESTOR"], users, authorities[authorityM])
    # addUser(GPP,'nhat','Nhatkey.txt', ["PROVIDER","OWNERPROJECT","SALEAGENT"], users, authorities[authorityM])
    # addUser(GPP,'bao','Baokey.txt', ["PROVIDER","DESIGNER","STAFF"], users, authorities[authorityM])
    # addUser(GPP,'kim','Kimkey.txt', ["PROVIDER","DESIGNER","MANAGER"], users, authorities[authorityM])
    # addUser(GPP,'luan','Luankey.txt', ["PROVIDER","CONSTRUCTION","MANAGER"], users, authorities[authorityM])
    # addUser(GPP,'thao','Thaokey.txt', ["PROVIDER","CONSTRUCTION","STAFF"], users, authorities[authorityM])
    # addUser(GPP,'an','Ankey.txt', ["PROVIDER","SUPERVISION","MANAGER"], users, authorities[authorityM])
    # addUser(GPP,'binh','Binhkey.txt', ["PROVIDER","SUPERVISION","STAFF"], users, authorities[authorityM])
    # addUser(GPP,'le','Lekey.txt', ['PUBLICADMIN','ADMINISTRATIVESTAFF'], users, authorities[authorityM])
    # addUser(GPP,'hanh','Hanhkey.txt', ['PUBLICADMIN','RECEIPTSTAFF'], users, authorities[authorityM])
    # addUser(GPP,'chau','Chaukey.txt', ['TRANSACTIONSUPPORT','SALEAGENTS'], users, authorities[authorityM])
    # addUser(GPP,'trung','Trungkey.txt', ['TRANSACTIONSUPPORT','CREDITAPPROVALOFFICER'], users, authorities[authorityM])
    # addUser(GPP,'nguyen','Nguyenkey.txt', ['TRANSACTIONSUPPORT','MANAGER'], users, authorities[authorityM])
#    addUser(GPP,'giang','Giangkey.txt', ['CUSTOMER','VIP'], users, authorities[authorityM])
#    addUser(GPP,'loc','Lockey.txt', ['CUSTOMER','NORMAL'], users, authorities[authorityM])

	# for attr in BobAttribute:
	# 	dac.keygen(GPP, aa1, attr, users[bob['id']], bob['authoritySecretKeys'])
	# writefile(alice,"Alicekey.txt")
	# writefile(bob,"Bobkey.txt")
#======================================
#=============Luke================
	# luke = { 'id': 'luke', 'authoritySecretKeys': {}, 'keys': None}
	# luke['keys'], users[luke['id']] = dac.registerUser(GPP)
	# for attr in LukeAttribute:
	# 	dac.keygen(GPP, aa1, attr, users[luke['id']], luke['authoritySecretKeys'])
	# writefile(luke,"Lukekey.txt")
	# print(luke)
#==============Other User==========
#	addUser(GPP,"john", "Johnkey.txt", JohnAttribute, users, aa1)
#	addUser(GPP,"lucy", "Lucykey.txt", LucyAttribute, users, aa1)
#	addUser(GPP, "fred" , "Fredkey.txt", FredAttribute, users, aa1)
#	addUser(GPP, "nick" , "Nickkey.txt", NickAttribute, users, aa1)
#	addUser(GPP, "mike" , "Mikekey.txt", MikeAttribute, users, aa1)
#	addUser(GPP, "lily" , "Lilykey.txt", LilyAttribute, users, aa1)
#    addUser(GPP,"nam", "Namkey.txt", NamAttribute, users, authorities[authority1])
#========
    # khanh = loadObject("Khanhkey.txt")
    # mai = loadObject("Maikey.txt")
    # Nam = loadObject("Namkey.txt")
    # mai = loadObject("Maikey.txt")
    # khanh = loadObject("Khanhkey.txt")
    # mai = loadObject("Maikey.txt")
    # khanh = loadObject("Khanhkey.txt")
    # mai = loadObject("Maikey.txt")
    # khanh = loadObject("Khanhkey.txt")
    # mai = loadObject("Maikey.txt")
    # khanh = loadObject("Khanhkey.txt")
    # mai = loadObject("Maikey.txt")
    # khanh = loadObject("Khanhkey.txt")
    # mai = loadObject("Maikey.txt")
    # khanh = loadObject("Khanhkey.txt")
    # mai = loadObject("Maikey.txt")
#	print(john)
    policy1 = "(OWNERPROJECT and (INVESTOR or BUSINESSMANAGER))"
    policy2 = "(OWNERPROJECT or (DESIGNER  and MANAGER))"
    policy3 = "(OWNERPROJECT or (CONSTRUCTION and MANAGER))"
    policy4 = "(OWNERPROJECT or  (SUPERVISION and MANAGER))"
    policy5 = "(PROVIDER or CUSTOMER)"
    policy6 = "(OWNERPROJECT)"
    policy7 = "(OWNERPROJECT or PUBLICADMIN or (CUSTOMER and VIP))"	
    policy8 = "(OWNERPROJECT or (PUBLICADMIN and (DIRECTOR or ADMINISTRATIVESTAFF)))"
    policy9 = "(OWNERPROJECT or PUBLICADMIN)"
    policy10 = "(OWNERPROJECT or (TRANSACTIONSUPPORT and (MANAGER or CREDITAPPROVALOFFICER)))"
    policy11 = "(OWNERPROJECT or TRANSACTIONSUPPORT or (CUSTOMER and VIP))"
    
    usernamelist = ['khanh','nam']
    listuser = []
#    listuser.append(khanh)
#    listuser.append(nam)
    listpolicy = []
    listpolicy.append(policy1)
    listpolicy.append(policy2)
    listpolicy.append(policy3)
    listpolicy.append(policy4)
    listpolicy.append(policy5)
    listpolicy.append(policy6)
    listpolicy.append(policy7)
    listpolicy.append(policy8)
    listpolicy.append(policy9)
    listpolicy.append(policy10)
    listpolicy.append(policy11)

    #=================Add key in list item =========================================
    # for i in range(1,101):
    #     filename= "document" + str(i) + ".json"
    #     print(filename)
    #     data = getvalueptfile(filename)
    #     # ab = {'Legal policy' : data['Public administration ']['Legal policy']}
    #     # data['Public administration ']['Legal policy'] = ab
    #     tm = data['Provider']['Product']
    #     for i in tm:
    #         ab = {i : tm[i]}
    #         data['Provider']['Product'][i] = ab
    #     addkeytodict(data['Provider']['Management and construction information'])
    #     addkeytodict(data['Provider']['Product'])
    #     addkeytodict2(data['Provider']['Information of user'],'Information of user')
    #     addkeytodict2(data['Public administration ']['Legal policy'],'Legal policy')
    #     addkeytodict2(data['Public administration ']['Information of user'],'Information of user')
    #     addkeytodict2(data['Transaction support party']['User Information'],'User Information')
    #     addkeytodict2(data['Transaction support party']['Patner Information'],'Patner Information')
    #     filename = "data/" + filename
    #     writefilejs(data,filename)
    # for i in range(2,101):
    #     filename= "document" + str(i) + ".json"
    #     print(filename)
    #     data = getvalueptfile(filename)
    #     addkeytodict2(data['Public administration ']['Type'],'Type')
    #     # k = data['Public administration ']['Type']
    #     # ab = {'Type' : k}
    #     # data['Public administration ']['Type'] = ab
    #     filename = "data/" + filename
    #     writefilejs(data,filename)
#    =================================Symetric Encypric AKO Generate file PT (with key unABEencrypted)====================================
    # for i in range (2,101):
    #     filename= "document" + str(i) + ".json"
    #     data = getvalueptfile(filename)
    #     print(filename)
    #     ab = data['Provider']
    #     for k in ab:
    #         if (k == 'Name Provider'):
    #             continue
    #         if (k == 'Management and construction information'):
    #             for j in ab[k]:
    #                 symeencrypt_value1(data['Provider'][k][j])
    #             continue
    #         symeencrypt_value1(data['Provider'][k])
    #     for k in data:
    #         if (k == 'Provider') or (k == 'id'):
    #             continue
    #         for j in data[k]:
    #             symeencrypt_value1(data[k][j])
    #     filename = "data/encrypted/" + "encrypted" + filename
    #     writefilejs(data,filename)
    # for i in range (1,2):
    #     filename= "document" + str(i) + ".json"
    #     data = getvalueptfile(filename)
    #     print(filename)
    #     ab = data['Provider']['Management and construction information']['Designer']['key']
    #     key = get_object_frombyte(ab)
    #     print(key)
    #====Encrypted Key =====
#     numberlist = [i for i in range(1,12)]   
#     listitem = {numberlist[i]: listpolicy[i] for i in range(len(numberlist))}
#     for i in range (1,101):
#         d = 1
#         filename = "encrypted/" + "encrypted" + "document" + str(i) + ".json"
#         print(filename)
#         data = getvalueptfile(filename)
#         ab = data['Provider']
#         for k in ab:
#             if (k == 'Management and construction information'):
#                 for j in ab[k]:
#                     if (encrypted_keywpc(GPP,authorities[authorityM],data['Provider'][k][j],d, listitem)):
#                         d += 1
#                 continue
#             if (encrypted_keywpc(GPP,authorities[authorityM],data['Provider'][k],d, listitem)):
#                 d += 1
#         for k in data:
#             if (k == 'Provider') or (k == 'id'):
#                 continue
#             for j in data[k]:
#                 if (encrypted_keywpc(GPP,authorities[authorityM],data[k][j],d, listitem)):
#                     d +=1
# #        print(json.dumps(data,indent=10))
#         filename = "data/" + filename
#         writefilejs(data,filename)
    #==========

    #==============================Encrypt Key && Upload to DatabaseCT=======
    # 	print(get_key("Contract5","Buyer detail"))
    # 	z = database.get_value("Contract5","Seller detail")
    # 	print(z.values())
    # 	policy1 = '(ALICE or BOB)'
    # 	key = get_key("Contract5", "Seller detail")
    # 	print("key", key)
    # #	print(aa1)

    # 	CT = dac.encrypt(GPP, policy1, key, aa1)
    # 	tmp = objectToBytes(CT,groupObj)
    # 	print("CT", CT)
    # 	database.uploaddbct("Document5","Seller detail", "key", tmp.decode('UTF-8'))
    #=========================================================================

    #==================Get Ciphertext Key from database CT ==============
    # k = database.get_keyct("Document5","Seller detail")
    # k = k.encode('UTF-8')
    # k = bytesToObject(k,groupObj)
    #	print(k)
    #=========================================================
    #=================SymetricEncryption Other Value && Upload DatabaseCT========================


    #======================SymetricEncrypt====

    #==============================
    #==================Do something ================================\
    ##################Go go ####################=======
    # listitem = {usernamelist[i]: listuser[i] for i in range(len(listuser))}
    # x = input("Name of User:")
    # y = input("Id of Document:")
    # y = "Document" + y
    # decrypt_documentbyuseraatrkey(GPP, listitem[x],y)
    #	print(aa1)
    #	setup_final(GPP, listpolicy, policy7 , aa1, "Document4")
    #=====================
    ####################=STEP SETUP FOR NEW DOCUMENT##############
    #==========Setup add key to DB PT=================
    #	setup_genkeyaddpt("Document1")
    #========================Create sapmle DB
    #	database.create_sampledbct("Document1")
    #============Encrypt key by ABE with policy=====
    #	encrypt_key_uploaddbct(GPP, "Document1",listpolicy, aa1)
    #============Syme encrypt value by key
    #	encrypt_value_uploaddb("Document1")
    #============Handle payments =======
    #	gen_addkey_symeencryptforpaym(GPP, "Document1", policy7,aa1)
if __name__ == '__main__':
    run()
