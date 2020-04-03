FROM tensorflow/tensorflow:1.14.0-gpu-py3

RUN apt-get update && apt-get install libsndfile1 -y

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]
