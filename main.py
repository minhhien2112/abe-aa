from charm.toolbox.eccurve import prime192v1
import abenc_dacmacs_yj14
from charm.toolbox.pairinggroup import PairingGroup, GT,extract_key
import json
from charm.core.engine.util import objectToBytes,bytesToObject
import pickle
from json import JSONEncoder 
import database
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
class value():
	def __init__(self):
		self.aa = loadObject("Authority.txt")
		self.alice = loadObject("Alicekey.txt")
		self.bob = loadObject("Bobkey.txt")
		self.luke = loadObject("Lukekey.txt")
		self.john = loadObject("Johnkey.txt")
		self.mike  = loadObject("Mikekey.txt")
		self.lucy = loadObject("Lucykey.txt")
		self.fred = loadObject("Fredkey.txt")
		self.nick = loadObject("Nickkey.txt")
		self.lily = loadObject("Lilykey.txt")
		self.usernamelist = ["alice", "bob","luke","john","mike","lucy","fred","nick","lily"]
		AliceAttribute = ["ALICE", "BUYER", "SELLER", "DOCTOR"]
		BobAttribute = ["BOB", "SELLER", "BUYER", "ENGINEER"]
		LukeAttribute =  ["LUKE", "SELLER", "OFFICESTAFF"]
		JohnAttribute =  ["CONSTRUCTION", "MANAGER"]
		MikeAttribute =  ["CONSTRUCTION", "FINANCE"]
		LucyAttribute = ["REALESTATE", "MANAGER"]  
		FredAttribute = ["EMPLOYEE", "CONSTRUCTION"]
		NickAttribute = ["REALESTATE", "EMPLOYEE"] 
		LilyAttribute =  ["REALESTATE", "FINANCE"]
		self.listattruser = []
		self.listattruser.append(AliceAttribute)
		self.listattruser.append(BobAttribute)
		self.listattruser.append(LukeAttribute)
		self.listattruser.append(JohnAttribute)
		self.listattruser.append(MikeAttribute)
		self.listattruser.append(LucyAttribute)
		self.listattruser.append(FredAttribute)
		self.listattruser.append(NickAttribute)
		self.listattruser.append(LilyAttribute)
		self.listuser = []
		self.listuser.append(self.alice)
		self.listuser.append(self.bob)
		self.listuser.append(self.luke)
		self.listuser.append(self.john)
		self.listuser.append(self.mike)
		self.listuser.append(self.lucy)
		self.listuser.append(self.fred)
		self.listuser.append(self.nick)
		self.listuser.append(self.lily)
	def checkattr(self,uname, listattr):
		listitem = {self.usernamelist[i]: self.listattruser[i] for i in range(len(self.listattruser))}
		for i in listattr:
			if (not i in listitem[uname]):
				print(i)
				return False
		return True
	def getukey(self,uname):
		listitem = {self.usernamelist[i]: self.listuser[i] for i in range(len(self.listuser))}
		return listitem[uname]
	def getciphertext(self,GPP,id,attributekey):
		res = {}
		for index in index_list:
			z = database.get_valuect(id, index)
			k = database.get_keyct(id,index)
			k = get_object_frombyte(k)
			TK = dac.checkat(GPP, k, attributekey['authoritySecretKeys'], attributekey['keys'][0])
		#	key = dac.decrypt(k, TK, attributekey['keys'][1])

			if (TK == False):
				z = dict.fromkeys(z, "*** NO PERMISSION ***")
				res[index] = z
				continue
			z['key'] = database.get_keyct(id,index)
			res[index] = z
		return res

def run():
	print("==============Run Program===========")
#	prepare()
#   ==============Get GPP From GPP.txt File =========
	# GPP_byte, GMK_byte = loadGPP()
	# GPP = bytesToObject(GPP_byte, groupObj)
	# GMK = bytesToObject(GMK_byte, groupObj)
#	print("GPP ",GPP)
#	print("GMK ", GMK)
	users = {}
	authorities = {}
	authorityAttributes = ["SELLER", "BUYER", "CONTRACTOR", \
	"DOCTOR", "ENGINEER", "EMPLOYEE", "ALICE" , "BOB", "LUKE", \
	"OFFICESTAFF", "MANAGER", "FINANCE", "CONSTRUCTION", "REALESTATE"]
	AliceAttribute = ["ALICE", "BUYER", "SELLER", "DOCTOR"]
	BobAttribute = ["BOB", "SELLER", "BUYER", "ENGINEER"]
	LukeAttribute =  ["LUKE", "SELLER", "OFFICESTAFF"]
	JohnAttribute =  ["CONSTRUCTION", "MANAGER"]
	MikeAttribute =  ["CONSTRUCTION", "FINANCE"]
	LucyAttribute = ["REALESTATE", "MANAGER"]  
	FredAttribute = ["EMPLOYEE", "CONSTRUCTION"]
	NickAttribute = ["REALESTATE", "EMPLOYEE"] 
	LilyAttribute =  ["REALESTATE", "FINANCE"]
#======================Setup Authority And Write to file ===========================
	# authority1 = "authority1"
	# dac.setupAuthority1(GPP, authority1, authorityAttributes, authorities)
	# print("Autority 1 ", authorities[authority1])
	# writefile(authorities[authority1],"Authority.txt")
	aa1 = loadObject("Authority.txt")
#	print(aa1)
#=============================Create User and write to file =======================
#======================Alice Bob========
	# alice = { 'id': 'alice', 'authoritySecretKeys': {}, 'keys': None}
	# alice['keys'], users[alice['id']] = dac.registerUser(GPP)
	# bob = { 'id': 'bob', 'authoritySecretKeys': {}, 'keys': None }
	# bob['keys'], users[bob['id']] = dac.registerUser(GPP)
	# for attr in AliceAttribute:
	# 	dac.keygen(GPP, aa1, attr, users[alice['id']], alice['authoritySecretKeys'])
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
#========
	alice = loadObject("Alicekey.txt")
	bob = loadObject("Bobkey.txt")
	luke = loadObject("Lukekey.txt")
	john = loadObject("Johnkey.txt")
	mike  = loadObject("Mikekey.txt")
	lucy = loadObject("Lucykey.txt")
	fred = loadObject("Fredkey.txt")
	nick = loadObject("Nickkey.txt")
	lily = loadObject("Lilykey.txt")
#	print(john)
	policy1 ='(LUKE or ALICE)'
	policy2 ='(LUKE or ALICE)'
	policy3 ='(LUKE or ALICE or REALESTATE)'
	policy4 ='(LUKE or ALICE or (REALESTATE and (MANAGER or FINANCE)))'
	policy5 ='(LUKE or ALICE or (REALESTATE and MANAGER))'
	policy6 ='(LUKE or ALICE or CONSTRUCTION)'
	policy7 ='(LUKE or ALICE or (CONSTRUCTION and MANAGER))'
	usernamelist = ["alice", "bob","luke","john","mike","lucy","fred","nick","lily"]
	listuser = []
	listuser.append(alice)
	listuser.append(bob)
	listuser.append(luke)
	listuser.append(john)
	listuser.append(mike)
	listuser.append(lucy)
	listuser.append(fred)
	listuser.append(nick)
	listuser.append(lily)
	listpolicy = []
	listpolicy.append(policy1)
	listpolicy.append(policy2)
	listpolicy.append(policy3)
	listpolicy.append(policy4)
	listpolicy.append(policy5)
	listpolicy.append(policy6)
#=================Add key in list item =========================================
	# key_list1 = ["Seller detail", "Buyer detail", "Property Detail", "Purchase price", "Construction detail"]
	# for i in key_list1:
	# 	k = groupObj.random(GT)
	# 	print(k)
	# 	tmp = objectToBytes(k, groupObj)
	# 	print(tmp.decode('UTF-8'))
	# 	database.add_key_value("Contract5",i,tmp.decode('UTF-8'))
	# 		# s = b'abc'
	# 		# print(s)
	# 		# s1 = s.decode('UTF-8')
	# 		# print(s1)
	# 		# s2 = s1.encode('UTF-8')
	# 		# print(s2)
#=====================================================================
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
#=====Decrypt key with Alice Key to gain symetric key ===============
	# TKalice = dac.generateTK(GPP, k, alice['authoritySecretKeys'], alice['keys'][0])
	# key = dac.decrypt(k, TKalice, alice['keys'][1])
	# TKbob = dac.generateTK(GPP, k, bob['authoritySecretKeys'], bob['keys'][0])
	# PTbob = dac.decrypt(k, TKbob, bob['keys'][1])
	# print(PT1a)
	# print(PTbob)
#======================SymetricEncrypt && Upload to DB=========
	# z = database.get_value("Contract5","Seller detail")
	# print(z)
	# a = SymmetricCryptoAbstraction(extract_key(key))
	# for i in z:
	# 	msg = z[i].encode('UTF-8')
	# 	ct = a.encrypt(msg)
	# 	ct = objectToBytes(ct,groupObj).decode('UTF-8')
	# 	database.uploaddbct("Document5","Seller detail", i, ct)
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
# if __name__ == '__main__':
# #	run()
# 	return
