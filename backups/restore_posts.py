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

def get_brisbane_time(dt):
    """Convert datetime to Brisbane timezone"""
    brisbane_tz = pytz.timezone('Australia/Brisbane')
    if dt.tzinfo is None:
        dt = timezone.make_aware(dt)
    return dt.astimezone(brisbane_tz)

def list_backup_files():
    """List all available backup files in chronological order"""
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        print("No backups directory found!")
        return []
    
    # Get all backup files
    backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.json')]
    if not backup_files:
        print("No backup files found!")
        return []
    
    # Sort files by date (newest first)
    backup_files.sort(reverse=True)
    
    print("\nAvailable backup files (newest first):")
    for i, file in enumerate(backup_files, 1):
        # Extract date from filename
        try:
            date_str = file.replace('posts_backup_', '').replace('.json', '')
            date_obj = datetime.strptime(date_str, "%Y-%m-%d_%H-%M-%S")
            brisbane_time = get_brisbane_time(date_obj)
            formatted_date = brisbane_time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{i}. {file} (Created: {formatted_date} Brisbane time)")
        except ValueError:
            print(f"{i}. {file}")
    
    return backup_files

def restore_from_backup(backup_file):
    """Restore posts from a backup file"""
    try:
        backup_path = os.path.join('backups', backup_file)
        with open(backup_path, 'r') as f:
            posts_data = json.load(f)
        
        restored_count = 0
        skipped_count = 0
        
        for post_data in posts_data:
            # Check if post already exists
            if Post.objects.filter(slug=post_data['slug']).exists():
                print(f"Skipping existing post: {post_data['title']}")
                skipped_count += 1
                continue
            
            # Get or create author
            author_data = post_data['author']
            author, created = Author.objects.get_or_create(
                first_name=author_data['first_name'],
                last_name=author_data['last_name'],
                email=author_data.get('email', '')
            )
            
            # Create post
            post = Post.objects.create(
                title=post_data['title'],
                excerpt=post_data['excerpt'],
                content=post_data['content'],
                slug=post_data['slug'],
                author=author,
                date=datetime.fromisoformat(post_data['date']) if post_data['date'] else timezone.now()
            )
            
            # Handle image if exists
            if post_data['image']:
                post.image.name = post_data['image']
                post.save()
            
            restored_count += 1
            print(f"Restored post: {post_data['title']}")
        
        print("\n=== Restore Summary ===")
        print(f"Total posts in backup: {len(posts_data)}")
        print(f"Successfully restored: {restored_count}")
        print(f"Skipped (already exist): {skipped_count}")
        print("=====================\n")
        
    except Exception as e:
        print(f"\nError during restore: {str(e)}")
        print("Please check the backup file and try again.\n")

def main():
    backup_files = list_backup_files()
    if not backup_files:
        return
    
    while True:
        try:
            choice = input("\nEnter the number of the backup file to restore (or 'q' to quit): ")
            if choice.lower() == 'q':
                break
            
            choice = int(choice)
            if 1 <= choice <= len(backup_files):
                restore_from_backup(backup_files[choice-1])
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number or 'q' to quit.")

if __name__ == "__main__":
    main() 