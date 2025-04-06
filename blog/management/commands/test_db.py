from django.core.management.base import BaseCommand
from django.db import connection
import time

class Command(BaseCommand):
    help = 'Test database connection'

    def handle(self, *args, **options):
        self.stdout.write('Testing database connection...')
        
        try:
            with connection.cursor() as cursor:
                start_time = time.time()
                cursor.execute("SELECT 1")
                end_time = time.time()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully connected to the database! '
                        f'Response time: {(end_time - start_time) * 1000:.2f}ms'
                    )
                )
                
                # Get database version
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                self.stdout.write(f'Database version: {version}')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to connect to the database: {str(e)}')
            ) 