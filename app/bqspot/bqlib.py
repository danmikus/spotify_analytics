from google.cloud import bigquery

def create_bq_client(path):
    client = bigquery.Client.from_service_account_json(path)

    return client

def create_taxonomy(bqclient, dataset_name, table_struct):

    dataset_list = [name.dataset_id for name in list(bqclient.list_datasets())]

    # Check if dataset name exists and if not, create it
    if dataset_name not in dataset_list:
        dataset_ref = bqclient.dataset(dataset_name)
        dataset = bigquery.Dataset(dataset_ref)
        dataset.description = 'Dataset for Analysis'
        dataset = bqclient.create_dataset(dataset)
    else:
        dataset_ref = bqclient.dataset(dataset_name)

    tables = [table.table_id for table in list(bqclient.list_tables(dataset_ref))]

    for item in table_struct:
        if item['name'] not in tables:
            table_ref = dataset_ref.table(item['name'])
            table = bigquery.Table(table_ref, schema=item['schema'])
            table.partitioning_type = 'DAY'
            table.partition_expiration = 2592000000
            bqclient.create_table(table)

def load_data(bqclient, data, dataset):

    dataset_ref = bqclient.dataset(dataset)

    for table_data in data:

        table_ref = dataset_ref.table(table_data['name'])
        table = bqclient.get_table(table_ref)
        bqclient.insert_rows(table, table_data['data'])
