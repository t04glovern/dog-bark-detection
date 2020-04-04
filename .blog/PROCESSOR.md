# FFMPEG Processor

Create Serverless Project

```bash
# Install Serverless framework
npm i -g serverless

# Create project
serverless create -t aws-python3 -n processor -p processor
cd processor
```

Add a new layer to the project by adding the following to the `serverless.yml` file

```yaml
layers:
  ffmpeg:
    path: layer
```

Then create a folder and include the layer build

```bash
mkdir layer && cd layer
curl -O https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
tar xf ffmpeg-git-amd64-static.tar.xz
rm ffmpeg-git-amd64-static.tar.xz
mv ffmpeg-git-*-amd64-static ffmpeg
cd ..
```

## Attribution

* [How to publish and use AWS Lambda Layers with the Serverless Framework](https://serverless.com/blog/publish-aws-lambda-layers-serverless-framework/)
