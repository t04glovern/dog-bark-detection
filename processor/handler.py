import boto3
import json
import os

queue_name = os.environ['QUEUE_NAME']

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

sqs_client = boto3.client('sqs')
response = sqs_client.get_queue_url(QueueName=queue_name)
queue_url = response['QueueUrl']

def upload_objects(root_path, bucket_name, out_dir):
    try:
        s3_bucket = s3_resource.Bucket(bucket_name)
        for path, subdirs, files in os.walk(root_path):
            path = path.replace("\\","/")
            directory_name = out_dir
            num_items = 0
            for file in files:
                num_items = num_items + 1
                s3_bucket.upload_file(os.path.join(path, file), directory_name + '/' + file, ExtraArgs={'ContentType': 'audio/wav'})
            return num_items
    except Exception as e:
        raise e

def process(event, context):

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    bucket_key = event['Records'][0]['s3']['object']['key']

    file_name_split = bucket_key.rsplit('/')
    file_name = file_name_split[2]
    file_name_no_ext = file_name.rsplit('.')[0]
    camera_name = file_name_split[0]
    file_unix_timestamp = file_name_no_ext[-10:]
    segment_time = '5'

    custom_path = '{}.{}.{}'.format(camera_name, file_unix_timestamp, segment_time)
    video_path = '/tmp/{}'.format(file_name)
    audio_path = '/tmp/{}'.format(custom_path)

    # Create the tmp directory
    os.system('mkdir {}'.format(audio_path))

    try:
        # Download video file to tmp location in lambda
        s3_client.download_file(bucket_name, bucket_key, video_path)
    except Exception as e:
        print('Error downloading s3://{}/{} : {}'.format(bucket_name, bucket_key, e))
        raise e

    try:
        # Convert video into audio segments of 5 seconds
        os.system('/opt/ffmpeg/ffmpeg -i {} -f segment -segment_time {} {}/%d.wav'.format(video_path, segment_time, audio_path))
        os.system('rm {}'.format(video_path))
    except Exception as e:
        print('Error converting video {} : {}'.format(video_path, e))
        raise e

    try:
        # Write fragments to S3
        processed_path = 'processed/{}'.format(custom_path)
        num_items = upload_objects(audio_path, bucket_name, processed_path)
        os.system('rm -rf {}'.format(audio_path))
    except Exception as e:
        print('Error uploading to s3 {} : {}'.format(audio_path, e))
        raise e

    # try:
    #     # Delete initial video file
    #     s3_client.delete_object(Bucket=bucket_name, Key=bucket_key)
    # except Exception as e:
    #     print('Error deleting from s3://{}/{} : {}'.format(bucket_name, bucket_key, e))
    #     raise e

    try:
        # Construct message
        message = {
            'camera': camera_name,
            'bucket_name': bucket_name,
            'bucket_path': processed_path,
            'num_items': num_items,
            'segment_length': segment_time,
            'timestamp': file_unix_timestamp
        }
        # Enqueue signal to process
        response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))
        return {
            'message': response
        }
    except Exception as e:
        print('Error queuing : {}'.format(e))
        raise e
