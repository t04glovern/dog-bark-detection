from keras.models import load_model
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

import librosa
import numpy as np

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

def extract_feature(file_name):

    try:
        audio_data, sample_rate = librosa.load(
            file_name, res_type='kaiser_fast')
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=40)
        mfccsscaled = np.mean(mfccs.T, axis=0)

    except Exception as e:
        print("Error encountered while parsing file: ", file_name)
        return None, None

    return np.array([mfccsscaled])


def print_prediction(file_name):
    prediction_feature = extract_feature(file_name)

    predicted_vector = model.predict_classes(prediction_feature)
    predicted_class = le.inverse_transform(predicted_vector)
    print("The predicted class is:", predicted_class[0], '\n')

    predicted_proba_vector = model.predict_proba(prediction_feature)
    predicted_proba = predicted_proba_vector[0]
    for i in range(len(predicted_proba)):
        category = le.inverse_transform(np.array([i]))
        print(category[0], "\t\t : ", format(predicted_proba[i], '.32f'))


# Custom Dog Bark
filename = './Evaluation audio/bell_bark_1.wav'
print_prediction(filename)
