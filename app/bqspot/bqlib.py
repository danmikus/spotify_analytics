from google.cloud import bigquery

def create_bq_client():
    client = bigquery.Client.from_service_account_json('credentials/bq_key.json')

if __name__ == "__main__":
    bq_client = create_bq_client()
