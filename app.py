from flask import Flask, render_template, request
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
region = os.environ.get('AWS_DEFAULT_REGION')

session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

s3 = session.client('s3')
rekognition = session.client('rekognition')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_image', methods=['POST'])
def process_image():
    image = request.files['image']

    image_key = 'uploads/' + image.filename
    s3.upload_fileobj(image, os.environ.get('S3_BUCKET_NAME'), image_key)

    rekognition
    resized_image = rekognition.detect_faces(
        Image={'S3Object': {'Bucket': os.environ.get('S3_BUCKET_NAME'), 'Name': image_key}},
        Attributes=['ALL']
    )

    processed_image_key = 'processed/' + image.filename
    s3.put_object(Body=resized_image, Bucket=os.environ.get('S3_BUCKET_NAME'), Key=processed_image_key)

    return render_template('result.html', image_key=processed_image_key)


if __name__ == '__main__':
    app.run(debug=True)
