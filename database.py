from azure.cosmos import exceptions, CosmosClient, PartitionKey
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.http_constants as http_constants
import family
from itertools import islice
import json
def take(n, iterable):
	"Return first n items of the iterable as a list"
	return list(islice(iterable, n))
url = "https://uitazurecosmosdb.documents.azure.com:443/"
key = 'egDOvxDLiwKxUgrmnpzG9BBhqpzenxpWMs1ODkPuRSEgDnLbYhJNhkDHd4Gq26prbIBYLRCtKVNQVusyQSnWmw=='
client = cosmos_client.CosmosClient(url, {'masterKey': key})
#"AzureSampleFamilyDatabase"
database = client.get_database_client("AzureSampleFamilyDatabase")
container = database.get_container_client("Contract")

databasect = client.get_database_client("ConstructionDocument")
containerct = databasect.get_container_client("Document")
def read_item(id):
    item_list = list(container.read_all_items(max_item_count=10))
    for doc in item_list:
        if (doc.get('id')== id):
            return doc
    print('Cannot found item with id', id)
def read_itemct(id):
    item_list = list(containerct.read_all_items(max_item_count=10))
    for doc in item_list:
        if (doc.get('id')== id):
            return doc
    print('Cannot found item with id', id)
def insert_database():
    container.upsert_item({
             'id': 'Contract6',
             'productName': 'Widget',
             'productModel': 'SN212314'
        })
def update_db_value(doc,k,value):
	doc[k]['key'] = value
	container.replace_item(item= doc, body = doc)
def update_db(doc,k):
	
	doc[k]['key'] = ''
	container.replace_item(item= doc, body = doc)
def createdtb():
	# keyList = ["Paras", "Jain", "Cyware"]
	# # initialize dictionary
	# d = {}
	# # iterating through the elements of list
	# for i in keyList:
	# 	d[i] = None
	# container_name = 'randomek'
	# container = database.create_container_if_not_exists(
	#     id=container_name, 
	#     partition_key=PartitionKey(path="/id"),
	#     offer_throughput=400
	# )
	item_list = list(container.read_all_items(max_item_count=10))
	print('Found {0} items'.format(item_list.__len__()))
	for doc in item_list:
		print('Item Id: {0}'.format(doc.get('id')))
		print(doc.keys())
		for i in doc:
			k = doc[i]
			if (type(k) == dict):
				print(k.keys())
				for x in k:
					tmp1 = k[x]
					if (type(tmp1) == dict):
						print(tmp1.keys())
						for y in k[x]:
							if (type(k[x][y]) == dict):
								print(k[x][y].keys())
								# for z in y:
								# 	if (type(y) == dict):
								# 		print(z.keys())
		# print(type(doc))
		# for i in doc:
		# 	print(i)
		# 	print(doc[i])
		# 	print("Type ", type(doc[i]))
		# 	if (type(doc[i]) == dict):
		# 		print(11)
		return
def uploaddbct(id, k, index, value):
	doc = read_itemct(id)
	doc[k][index] = value
	containerct.replace_item(item= doc, body = doc)
	return
def add_key(id):
	key_list1 = ["Seller detail", "Buyer detail", "Property Detail", "Purchase price", "Contractors detail"]
	doc = read_item(id)
	for k in doc:
		print(k)
		if (k in key_list1):
			update_db(doc,k)
def add_key_value(id, k, value):
	doc = read_item(id)
	update_db_value(doc,k,value)
def add_key_tandpay(id):
	doc = read_item(id)
	doc['Time and payments']['Time']['key'] = ''
	doc['Time and payments']['Payments']['key'] = ''
	container.replace_item(item= doc, body = doc)
	return
def get_keyct(id,k):
	doc = read_itemct(id)
	return doc[k]['key']
def get_key(id,k):
	doc = read_item(id)
	return doc[k]['key']
def get_keypm(x,id):
	if x == 1:
		doc = read_item(id)
	else:
		doc = read_itemct(id)
	return doc["Construction detail"]["Payments"]["key"]
def get_value(id,k):
	doc = read_item(id)
	del doc[k]['key']
	return doc[k]
def get_value_pm(x,id):
	if x == 1:
		doc = read_item(id)
	else:
		doc = read_itemct(id)
	doc = doc["Construction detail"]["Payments"]
	del doc["key"]
	return doc
def upload_value_pmct(id,k,value):
	doc = read_itemct(id)
	doc["Construction detail"]["Payments"][k] = value
	containerct.replace_item(item= doc, body = doc)
def get_valuect(id,k):
	doc = read_itemct(id)
	del doc[k]['key']
	return doc[k]
def create_sampledbct(id):
	db = read_item(id)
	containerct.create_item(body=db)
def upload_keypaym(x, id,value):
	if x == 1:
		doc = read_item(id)
		cont = container
	else:
		cont = containerct
		doc = read_itemct(id)
	doc["Construction detail"]["Payments"]["key"] = value
	cont.replace_item(item= doc, body = doc)
	return
#if __name__ == '__main__':
	#createdtb()
	#createdtb()
	#insert_database()
#	read_item('Contract5')
	# add_key('Contract5')
	# add_key_tandpay('Contract5')