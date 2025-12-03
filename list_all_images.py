#!/usr/bin/env python
"""
Script to list all images in the database
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myProject.settings')
django.setup()

from myApp.models import MediaAsset

print("=" * 60)
print("All Images in Database:")
print("=" * 60)

all_images = MediaAsset.objects.all().order_by('-created_at')

if all_images.count() == 0:
    print("No images found in database.")
    print("\nPlease upload images through the dashboard at:")
    print("  http://localhost:8000/dashboard/gallery/")
else:
    for idx, img in enumerate(all_images, 1):
        print(f"\n{idx}. Title: {img.title}")
        print(f"   Description: {img.description[:50] if img.description else 'N/A'}")
        print(f"   URL: {img.original_url}")
        print(f"   Created: {img.created_at}")

print("\n" + "=" * 60)

