from google.cloud import bigquery

def create_bq_client():
    client = bigquery.Client.from_service_account_json('credentials/bq_key.json')

    return client

def dataset_creation(client, dataset_name):
    dataset_list = [name.dataset_id for name in list(client.list_datasets())]

    if dataset_name not in dataset_list:
        dataset_ref = client.dataset(dataset_name)
        dataset = bigquery.Dataset(dataset_ref)
        dataset.description = 'Dataset for Spotify Analysis'
        dataset = client.create_dataset(dataset)

if __name__ == "__main__":
    bq_client = create_bq_client()
    dataset_name = "spotify_dataset"

    dataset_creation(bq_client, dataset_name)
