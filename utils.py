import boto3
import os
import tempfile
import librosa

queue_name = os.environ['QUEUE_NAME']

sqs_client = boto3.client('sqs')
response = sqs_client.get_queue_url(QueueName=queue_name)
queue_url = response['QueueUrl']

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

def download_wav_data(bucket, bucket_key):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    object = bucket.Object(bucket_key)
    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'wb') as f:
        object.download_fileobj(f)
        try:
            audio_data, sample_rate = librosa.load(tmp.name, res_type='kaiser_fast')
        except Exception as e:
            print('ERROR: WAV file sampling failed')
            print(e)
            raise e
        return audio_data, sample_rate
