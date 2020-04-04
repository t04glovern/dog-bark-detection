import boto3
import json
import os

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

def upload_objects(root_path, bucket_name, out_dir):
    try:
        s3_bucket = s3_resource.Bucket(bucket_name)
        for path, subdirs, files in os.walk(root_path):
            path = path.replace("\\","/")
            directory_name = out_dir
            for file in files:
                s3_bucket.upload_file(os.path.join(path, file), directory_name + '/' + file)
    except Exception as e:
        raise e

def process(event, context):

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    bucket_key = event['Records'][0]['s3']['object']['key']

    file_name_no_ext = bucket_key.rsplit('.', 1)[0]
    camera_name = file_name_no_ext[0:8]
    file_unix_timestamp = file_name_no_ext[-10:]
    segment_time = '5'

    custom_path = '{}.{}.{}'.format(camera_name, file_unix_timestamp, segment_time)
    video_path = '/tmp/{}{}'.format(file_unix_timestamp, bucket_key)
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
        os.system('/opt/ffmpeg/ffmpeg -i {} -f segment -segment_time {} -c copy {}/%09d.wav'.format(video_path, segment_time, audio_path))
    except Exception as e:
        print('Error converting video {} : {}'.format(video_path, e))
        raise e

    try:
        # Write fragments to S3
        upload_objects(audio_path, bucket_name, custom_path)
    except Exception as e:
        print('Error uploading to s3 {} : {}'.format(audio_path, e))
        raise e

    try:
        # Delete initial video file
        s3_client.delete_object(Bucket=bucket_name, Key=bucket_key)
    except Exception as e:
        print('Error deleting from s3://{}/{} : {}'.format(bucket_name, bucket_key, e))
        raise e

    body = {
        "message": "Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
