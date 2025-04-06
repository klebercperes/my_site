import os
import json
import django
import sys
from datetime import datetime
import pytz
from django.utils import timezone

# Add the project directory to the Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_site.settings')
django.setup()

# Now we can import Django models
from blog.models import Post, Author

def create_backup_directory():
    """Create a backup directory if it doesn't exist"""
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    return backup_dir

def get_backup_data():
    """Get all posts and prepare them for backup"""
    posts = Post.objects.all()
    posts_data = []
    
    for post in posts:
        post_data = {
            'title': post.title,
            'excerpt': post.excerpt,
            'content': post.content,
            'slug': post.slug,
            'image': post.image.name if post.image else None,
            'author': {
                'first_name': post.author.first_name,
                'last_name': post.author.last_name,
                'email': post.author.email
            },
            'date': post.date.isoformat() if post.date else None
        }
        posts_data.append(post_data)
    
    return posts_data

def get_brisbane_time():
    """Get current time in Brisbane timezone"""
    brisbane_tz = pytz.timezone('Australia/Brisbane')
    return timezone.now().astimezone(brisbane_tz)

def main():
    try:
        # Create backup directory
        backup_dir = create_backup_directory()
        
        # Get backup data
        posts_data = get_backup_data()
        
        # Get current time in Brisbane
        current_time = get_brisbane_time()
        
        # Create backup filename with readable date and time
        backup_filename = f'posts_backup_{current_time.strftime("%Y-%m-%d_%H-%M-%S")}.json'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Save to JSON file
        with open(backup_path, 'w') as f:
            json.dump(posts_data, f, indent=4)
        
        # Print summary
        print("\n=== Backup Summary ===")
        print(f"Backup created successfully: {backup_path}")
        print(f"Backup time (Brisbane): {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Number of posts backed up: {len(posts_data)}")
        print(f"Backup size: {os.path.getsize(backup_path) / 1024:.2f} KB")
        print("===================\n")
        
    except Exception as e:
        print(f"\nError during backup: {str(e)}")
        print("Please check your database connection and try again.\n")

if __name__ == "__main__":
    main() 