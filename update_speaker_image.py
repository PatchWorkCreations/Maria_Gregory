#!/usr/bin/env python
"""
Script to update About section with Speaker image
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myProject.settings')
django.setup()

from myApp.models import MediaAsset, About

print("=" * 60)
print("Searching for Speaker image...")
print("=" * 60)

# Find the Speaker image - try multiple search patterns
speaker = None
search_terms = ['Speaker', 'speaker', 'SPEAKER', 'WhyYou', 'Mentor', 'Sponsor', 'Why You']

# First, list all images to help debug
all_images = MediaAsset.objects.all()
print(f"\nTotal images in database: {all_images.count()}\n")

if all_images.count() > 0:
    print("Available images:")
    for img in all_images:
        print(f"  - ID: {img.id}, Title: '{img.title}'")
    print()

# Try to find Speaker image
for term in search_terms:
    speaker = MediaAsset.objects.filter(title__icontains=term).first()
    if speaker:
        print(f"Found image matching '{term}': {speaker.title}")
        break

if speaker:
    # Get or create About section
    about, created = About.objects.get_or_create(pk=1)
    
    # Update image URL (prefer web_url if available, otherwise original_url)
    about.image_url = speaker.web_url if speaker.web_url else speaker.original_url
    about.save()
    
    print("\n" + "=" * 60)
    print("SUCCESS: Updated About section with Speaker image!")
    print("=" * 60)
    print(f"  Image URL: {about.image_url}")
    print(f"  Image Title: {speaker.title}")
    print(f"  Image ID: {speaker.id}")
    print("\nThe image should now appear on your homepage!")
else:
    print("\n" + "=" * 60)
    print("ERROR: Could not find image with title containing 'Speaker'")
    print("=" * 60)
    if all_images.count() == 0:
        print("\nNo images found in database.")
        print("\nPlease:")
        print("  1. Go to http://localhost:8000/dashboard/gallery/")
        print("  2. Upload your 'Speaker' image")
        print("  3. Run this script again: python update_speaker_image.py")
    else:
        print("\nPlease check the image title in the dashboard and ensure")
        print("it contains 'Speaker' in the title.")

