import os
from django.core.management.base import BaseCommand
from django.conf import settings
import boto3

class Command(BaseCommand):
    help = 'Upload static files directly to S3'

    def handle(self, *args, **options):
        # Initialize S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        # Get the static files directory
        static_dir = settings.STATICFILES_DIRS[0]
        
        self.stdout.write(f'Uploading files from {static_dir} to S3...')

        # Walk through the static directory
        for root, dirs, files in os.walk(static_dir):
            for file in files:
                # Get the full local path
                local_path = os.path.join(root, file)
                
                # Get the relative path from the static directory
                relative_path = os.path.relpath(local_path, static_dir)
                
                # Create the S3 key (path in the bucket)
                s3_key = f'static/{relative_path}'
                
                self.stdout.write(f'Uploading {relative_path} to {s3_key}...')
                
                # Upload the file
                with open(local_path, 'rb') as f:
                    s3.upload_fileobj(
                        f,
                        settings.AWS_STORAGE_BUCKET_NAME,
                        s3_key
                    )
                
                self.stdout.write(self.style.SUCCESS(f'Successfully uploaded {s3_key}')) 