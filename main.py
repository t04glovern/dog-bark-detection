from keras.models import load_model
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

from utils import get_messages_from_queue, download_wav_data

import librosa
import numpy as np
import json
import boto3
import os
import time

region = os.environ['AWS_DEFAULT_REGION']
table_name = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

# Label list
class_lables = [
    "air_conditioner",
    "car_horn",
    "children_playing",
    "dog_bark",
    "drilling",
    "engine_idling",
    "gunshot",
    "jackhammer",
    "siren",
    "street_music"
]

# load model
model = load_model('./model/weights.hdf5')

# Encode the classification labels
le = LabelEncoder()
y = np.array(class_lables)
yy = to_categorical(le.fit_transform(y))

def extract_feature(audio_data, sample_rate):

    try:
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=40)
        mfccsscaled = np.mean(mfccs.T, axis=0)

    except Exception as e:
        print("Error encountered while parsing file: ", file_name)
        return None, None

    return np.array([mfccsscaled])


def return_prediction(audio_data, sample_rate):
    prediction_feature = extract_feature(audio_data, sample_rate)
    predicted_vector = model.predict_classes(prediction_feature)
    predicted_class = le.inverse_transform(predicted_vector)
    predicted_proba_vector = model.predict_proba(prediction_feature)
    predicted_proba = predicted_proba_vector[0]
    prediction = {
        'class': predicted_class[0],
        'probabilities': {
            'air_conditioner': predicted_proba[0],
            'car_horn': predicted_proba[1],
            'children_playing': predicted_proba[2],
            'dog_bark': predicted_proba[3],
            'drilling': predicted_proba[4],
            'engine_idling': predicted_proba[5],
            'gunshot': predicted_proba[6],
            'jackhammer': predicted_proba[7],
            'siren': predicted_proba[8],
            'street_music': predicted_proba[9]
        }
    }
    return prediction

def main():
    while True:
        time.sleep(5)
        messages = get_messages_from_queue()
        print('[INFO] Retrieved ' + str(len(messages)) + ' messages')

        # Process each message
        for message in messages:
            try:
                try:
                    body = json.loads(message['Body'])
                    print(body)
                    camera = body['camera']
                    bucket = body['bucket_name']
                    bucket_path = body['bucket_path']
                    num_items = int(body['num_items'])
                    segment_length = int(body['segment_length'])
                    timestamp = int(body['timestamp'])
                except Exception as e:
                    print()
                    print('ERROR: Parsing message')
                    print(e)
                    raise e
    
                try:
                    for i in range(num_items):
                        try:
                            wav_file_key = '{}/{}.wav'.format(bucket_path, i)
                            audio_data, sample_rate = download_wav_data(bucket, wav_file_key)
                            prediction = return_prediction(audio_data, sample_rate)
                            prediction['timestamp'] = timestamp + (i * segment_length)
                            if prediction['class'] == 'dog_bark' and prediction['probabilities']['dog_bark'] > 0.75:
                                try:
                                    table.put_item(
                                        Item={
                                            'camera': camera,
                                            'timestamp': prediction['timestamp'],
                                            'probability': format(prediction['probabilities']['dog_bark'], '.32f'),
                                            'wav_file': 'https://{}.s3-{}.amazonaws.com/{}'.format(bucket, region, wav_file_key)
                                        }
                                    )
                                except Exception as e:
                                    print('ERROR: Inserting in DynamoDB')
                                    print(e)
                        except Exception as e:
                            print('ERROR: Decoding WAV data')
                            print(e)
                except Exception as e:
                    print('ERROR: Downloading WAV file')
                    print(e)
                    raise e

            except Exception as e:
                print('FATAL ERROR')
                print(e)

if __name__ == '__main__':
    main()