from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
import boto3
import os
import uuid
from dotenv import load_dotenv
from mangum import Mangum
import requests


app = FastAPI()
load_dotenv()

ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

@app.post("/predict_nsfw_image/")
async def upload_image(file: UploadFile):
    try:
        # Initialize the S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
        )

        # Generate a unique filename
        file_name = str(uuid.uuid4()) + file.filename

        # Define the ACL for the S3 object (e.g., 'public-read' for public access)
        acl = 'public-read'

        # Upload the file to S3 with the specified ACL
        s3.upload_fileobj(
            file.file,
            S3_BUCKET_NAME,
            file_name,
            ExtraArgs={'ACL': acl}  # Specify the ACL here
        )

        # Generate the S3 URL for the uploaded file
        s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file_name}"

        url = 'https://32nuexpwcubkn7226zluwfe7yi0eewqf.lambda-url.eu-north-1.on.aws/predict_nsfw_images'
        params = {
            'unique_id': '132',
            'image_urls': s3_url
        }

        headers = {
            'accept': 'application/json',
        }

        response = requests.post(url, params=params, headers=headers)

        return JSONResponse(content={"message": "Image uploaded successfully", "output": response.json()}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

handler = Mangum(app)
