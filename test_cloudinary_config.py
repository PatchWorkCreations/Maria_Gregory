#!/usr/bin/env python
"""
Quick test to verify Cloudinary configuration is working
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myProject.settings')
django.setup()

print("=" * 60)
print("Cloudinary Configuration Test")
print("=" * 60)

# Check environment variables
cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME', '')
api_key = os.getenv('CLOUDINARY_API_KEY', '')
api_secret = os.getenv('CLOUDINARY_API_SECRET', '')

print("\nEnvironment Variables:")
print("-" * 60)

if cloud_name:
    print(f"[OK] CLOUDINARY_CLOUD_NAME: {cloud_name}")
else:
    print("[X] CLOUDINARY_CLOUD_NAME: NOT SET")

if api_key:
    print(f"[OK] CLOUDINARY_API_KEY: {api_key[:10]}...")
else:
    print("[X] CLOUDINARY_API_KEY: NOT SET")

if api_secret:
    print(f"[OK] CLOUDINARY_API_SECRET: {api_secret[:10]}...")
else:
    print("[X] CLOUDINARY_API_SECRET: NOT SET")

print("\n" + "-" * 60)
print("Configuration Status:")
print("-" * 60)

if cloud_name and api_key and api_secret:
    print("[OK] All Cloudinary credentials are configured!")
    print("\nIf you're still getting errors:")
    print("1. Make sure you RESTARTED your Django server after adding credentials")
    print("2. Stop the server (Ctrl+C) and start it again: python manage.py runserver")
else:
    print("[X] Missing Cloudinary credentials!")
    print("\nMake sure your .env file contains:")
    print("CLOUDINARY_CLOUD_NAME=your_cloud_name")
    print("CLOUDINARY_API_KEY=your_api_key")
    print("CLOUDINARY_API_SECRET=your_api_secret")

print("\n" + "=" * 60)

