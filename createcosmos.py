from azure.cosmos import exceptions, CosmosClient, PartitionKey
import family
# Initialize the Cosmos client
endpoint = "https://uitazurecosmosdb.documents.azure.com:443/"
key = 'egDOvxDLiwKxUgrmnpzG9BBhqpzenxpWMs1ODkPuRSEgDnLbYhJNhkDHd4Gq26prbIBYLRCtKVNQVusyQSnWmw=='
endpoint2 = 'mongodb://azuremongodbapiuit:U6csdImtbMLBeZsZIrPKElEncQcazEfDgUHrzsLrjYnEAgnMM3Pimjl0HSWKoUe0bxQLsiQ5bsu0SKb4HlRXQg==@azuremongodbapiuit.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@azuremongodbapiuit@'
key2 = 'U6csdImtbMLBeZsZIrPKElEncQcazEfDgUHrzsLrjYnEAgnMM3Pimjl0HSWKoUe0bxQLsiQ5bsu0SKb4HlRXQg=='
# <create_cosmos_client>
client = CosmosClient(endpoint2, key2)
# </create_cosmos_client>

# Create a database
# <create_database_if_not_exists>
database_name = 'ConstructionDocument'
database = client.create_database_if_not_exists(id=database_name)
# </create_database_if_not_exists>

# Create a container
# Using a good partition key improves the performance of database operations.
# <create_container_if_not_exists>
container_name = 'Document'
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)
# </create_container_if_not_exists>


# Add items to the container
# family_items_to_create = [family.get_andersen_family_item(), family.get_johnson_family_item(), family.get_smith_family_item(), family.get_wakefield_family_item()]
# print(type(family_items_to_create[0]))
#  # <create_item>
# for family_item in family_items_to_create:
#     container.create_item(body=family_item)
# # </create_item>

# # Read items (key value lookups by partition key and id, aka point reads)
# # <read_item>
# for family in family_items_to_create:
#     item_response = container.read_item(item=family['id'], partition_key=family['lastName'])
#     request_charge = container.client_connection.last_response_headers['x-ms-request-charge']
#     print('Read item with id {0}. Operation consumed {1} request units'.format(item_response['id'], (request_charge)))
# # </read_item>

# # Query these items using the SQL query syntax. 
# # Specifying the partition key value in the query allows Cosmos DB to retrieve data only from the relevant partitions, which improves performance
# # <query_items>
# query = "SELECT * FROM c WHERE c.lastName IN ('Wakefield', 'Andersen')"

# items = list(container.query_items(
#     query=query,
#     enable_cross_partition_query=True
# ))

# request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

# print('Query returned {0} items. Operation consumed {1} request units'.format(len(items), request_charge))
# # </query_items>