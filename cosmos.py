from azure.cosmos import exceptions, CosmosClient, PartitionKey
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.http_constants as http_constants
import json
# Enumerate the returned items
url = "https://uitazurecosmosdb.documents.azure.com:443/"
key = 'egDOvxDLiwKxUgrmnpzG9BBhqpzenxpWMs1ODkPuRSEgDnLbYhJNhkDHd4Gq26prbIBYLRCtKVNQVusyQSnWmw=='
client = cosmos_client.CosmosClient(url, {'masterKey': key})
container_id = "Persons"
database_id = "SampleDB"
#"AzureSampleFamilyDatabase"
database = client.get_database_client("SampleDB")
container = database.get_container_client("Persons")
def list_items(id):
    item_list = list(container.read_all_items(max_item_count=10))
    print('Found {0} items'.format(item_list.__len__()))
    for doc in item_list:
        if (doc.get('id')== id):
            print(doc)
            return
    print('Cannot found item with id', id)

def check_existed(container, doc_id):
    item_list = list(container.read_all_items(max_item_count=10))
    kt = False
    for doc in item_list:
        print(doc.get('id'))
        if (doc.get('id') == doc_id):
            kt = True
            break
    return kt
def update_items(container,doc_id):
    if check_existed(container,doc_id) == False:
        print("Doc id no existed in Container")
        return
    body = {
            'firstname' : "Item0"
    }
    container.replace_item(item=doc_id, body=body)
def query_database(client):
    for item in container.query_items(query='SELECT * FROM container_id'\
        , enable_cross_partition_query=True):
        print(json.dumps(item, indent=True))
def insert_database(client):
    container.upsert_item({
             'id': 'item{0}'.format(0),
             'productName': 'Widget',
             'productModel': 'Model {0}'.format(0)
        })
def list_databases(client):
    print("\n4. List all Databases on an account")
    print('Databases:')

    databases = list(client.list_databases())

    if not databases:
        return

    for database in databases:
        print(database['id'])

def run():
    # Initialize the Cosmos client
    # print("List Database")
    # list_databases(client)
    # print("Update Item")
    # list_items(container)
#   read_items(container)
#   read_item(container,"Item1")
    # print("Read Database")
    # query_database(client)
    # print("Insert DB")
    # insert_database(client)
    # print("Read Database")
    # query_database(client)    
#    read_database(client,"SampleDB")
    # </query_items>
if __name__ == '__main__':
    run()