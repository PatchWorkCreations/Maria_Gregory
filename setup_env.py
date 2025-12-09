#!/usr/bin/env python
"""
Interactive script to help create .env file
"""
import os

def create_env_file():
    """Create .env file with user input"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    # Check if .env already exists
    if os.path.exists(env_path):
        print("=" * 60)
        print("WARNING: .env file already exists!")
        print("=" * 60)
        response = input("Do you want to overwrite it? (yes/no): ").strip().lower()
        if response != 'yes':
            print("Cancelled. Existing .env file preserved.")
            return
    
    print("=" * 60)
    print("Cloudinary Setup")
    print("=" * 60)
    print("\nTo get your Cloudinary credentials:")
    print("1. Go to: https://cloudinary.com/console")
    print("2. Sign up for a free account (if you don't have one)")
    print("3. Copy your credentials from the dashboard")
    print("\n" + "-" * 60)
    
    # Get Cloudinary credentials
    print("\nEnter your Cloudinary credentials:")
    cloud_name = input("Cloud Name: ").strip()
    api_key = input("API Key: ").strip()
    api_secret = input("API Secret: ").strip()
    
    # Optional OpenAI key
    print("\n" + "-" * 60)
    print("OpenAI API Key (optional - press Enter to skip):")
    openai_key = input("OpenAI API Key: ").strip()
    
    # Create .env content
    env_content = f"""# Cloudinary Configuration
# Get these from: https://cloudinary.com/console
CLOUDINARY_CLOUD_NAME={cloud_name}
CLOUDINARY_API_KEY={api_key}
CLOUDINARY_API_SECRET={api_secret}

# OpenAI Configuration (optional)
OPENAI_API_KEY={openai_key if openai_key else 'your_openai_api_key_here'}
"""
    
    # Write .env file
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print("\n" + "=" * 60)
        print("SUCCESS: .env file created!")
        print("=" * 60)
        print(f"\nFile created at: {env_path}")
        print("\nNext steps:")
        print("1. Verify your credentials are correct")
        print("2. Restart your Django server: python manage.py runserver")
        print("3. Try uploading an image in the dashboard")
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\nERROR: Could not create .env file: {e}")
        print("\nPlease create it manually with the following content:")
        print("-" * 60)
        print(env_content)
        print("-" * 60)

if __name__ == '__main__':
    create_env_file()



