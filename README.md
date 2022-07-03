# Dog Bark Detection

![Architecture Diagram](assets/bark-detector.png)

## Conda Environment

```bash
conda env create -f environment.yml
conda activate dog-bark
```

## Basic Exploration
If you're just looking to play around with the ML model without worrying
about the AWS cloud components I'd strongly suggest looking at 
[notebook.ipyn](notebook.ipynb) after running the conda commands.
It's set up to train the model from scratch and run inference over `.wav` files.

### Run Prediction

```bash
QUEUE_NAME=<queue_name> TABLE_NAME=<table_name> python3 main.py
```

## Docker

```bash
docker build -t dog-bark .
docker run --env QUEUE_NAME=<queue_name> --env TABLE_NAME=<table_name> dog-bark
```

### ECS

```bash
# Login
aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.ap-southeast-2.amazonaws.com/dog-bark-detection

# Build
docker build -t dog-bark-detection .
docker tag dog-bark-detection:latest \
    123456789012.dkr.ecr.ap-southeast-2.amazonaws.com/dog-bark-detection:latest
# Push
docker push 123456789012.dkr.ecr.ap-southeast-2.amazonaws.com/dog-bark-detection:latest
```

### Kubernetes

```bash
gcloud auth login
gcloud config set project <PROJECT>

docker build -t gcr.io/<PROJECT>/bark-detector:latest .
docker push gcr.io/<PROJECT>/bark-detector:latest

# When connected to Kubernetes
kubectl apply -f deploy.yml
```

## Attribution

* [Sound Classification using Deep Learning](https://medium.com/@mikesmales/sound-classification-using-deep-learning-8bc2aa1990b7)
