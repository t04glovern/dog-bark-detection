import boto3
from datetime import datetime
import os
import tempfile
import librosa

queue_name = os.environ['QUEUE_NAME']

# SQS Client
sqs_client = boto3.client('sqs')
response = sqs_client.get_queue_url(QueueName=queue_name)
queue_url = response['QueueUrl']

# CloudWatch Client
cloudwatch_client = boto3.client('cloudwatch')

# S3 Client
s3_client = boto3.resource('s3')

def get_messages_from_queue():
    messages = []

    while True:
        resp = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=1
        )

        try:
            messages.extend(resp['Messages'])
        except KeyError:
            break

        entries = [
            {'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
            for msg in resp['Messages']
        ]

        resp = sqs_client.delete_message_batch(
            QueueUrl=queue_url, Entries=entries
        )

        if len(resp['Successful']) != len(entries):
            raise RuntimeError(
                "Failed to delete messages: entries={entries} resp={resp}"
            )

    return messages

def download_wav_data(bucket_name, bucket_key):
    bucket = s3_client.Bucket(bucket_name)
    object = bucket.Object(bucket_key)
    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'wb') as f:
        object.download_fileobj(f)
        try:
            audio_data, sample_rate = librosa.load(tmp.name, res_type='kaiser_fast')
        except Exception as e:
            print('ERROR: WAV file sampling failed : {}'.format(bucket_key))
            print(e)
            raise e
        return audio_data, sample_rate

def put_bark_metric(timestamp, probability):
    try:
        cloudwatch_client.put_metric_data(
            MetricData = [
                {
                    'MetricName': 'Bark',
                    'Dimensions': [
                        {
                            'Name': 'PROBABILITY',
                            'Value': probability
                        }
                    ],
                    'Timestamp': datetime.fromtimestamp(timestamp),
                    'Unit': 'None',
                    'Value': 1
                },
            ],
            Namespace='DogBarkDetector'
        )
    except Exception as e:
        print('ERROR: Putting metric to CloudWatch')
        print(e)
