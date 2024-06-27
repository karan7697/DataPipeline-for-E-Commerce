import json
import psycopg2
import os

def lambda_handler(event, context):
    conn = psycopg2.connect(
        dbname=os.getenv('REDSHIFT_DB'),
        user=os.getenv('REDSHIFT_USER'),
        password=os.getenv('REDSHIFT_PASS'),
        host=os.getenv('REDSHIFT_HOST'),
        port=os.getenv('REDSHIFT_PORT')
    )
    cursor = conn.cursor()
    
    for record in event['Records']:
        payload = json.loads(record['kinesis']['data'])
        cursor.execute(
            "INSERT INTO ecommerce_data (event_time, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
            (payload['event_time'], payload['product_id'], payload['quantity'], payload['price'])
        )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data processed successfully!')
    }
