#!/usr/bin/env python
"""
Diagnostic script to check upload configuration
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myProject.settings')
django.setup()

print("=" * 60)
print("Upload Configuration Diagnostic")
print("=" * 60)

# Check .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    print("\n✓ .env file exists")
    with open(env_path, 'r') as f:
        content = f.read()
        if 'CLOUDINARY_CLOUD_NAME' in content:
            print("  [OK] Contains CLOUDINARY_CLOUD_NAME")
        else:
            print("  [X] Missing CLOUDINARY_CLOUD_NAME")
        if 'CLOUDINARY_API_KEY' in content:
            print("  [OK] Contains CLOUDINARY_API_KEY")
        else:
            print("  [X] Missing CLOUDINARY_API_KEY")
        if 'CLOUDINARY_API_SECRET' in content:
            print("  [OK] Contains CLOUDINARY_API_SECRET")
        else:
            print("  [X] Missing CLOUDINARY_API_SECRET")
else:
    print("\n[X] .env file NOT FOUND")
    print("  This is likely why uploads are failing!")

# Check environment variables
print("\n" + "-" * 60)
print("Environment Variables:")
print("-" * 60)

cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME', '')
api_key = os.getenv('CLOUDINARY_API_KEY', '')
api_secret = os.getenv('CLOUDINARY_API_SECRET', '')

if cloud_name:
    print(f"[OK] CLOUDINARY_CLOUD_NAME: {cloud_name[:10]}..." if len(cloud_name) > 10 else f"[OK] CLOUDINARY_CLOUD_NAME: {cloud_name}")
else:
    print("[X] CLOUDINARY_CLOUD_NAME: NOT SET")

if api_key:
    print(f"[OK] CLOUDINARY_API_KEY: {api_key[:10]}..." if len(api_key) > 10 else f"[OK] CLOUDINARY_API_KEY: {api_key}")
else:
    print("[X] CLOUDINARY_API_KEY: NOT SET")

if api_secret:
    print(f"[OK] CLOUDINARY_API_SECRET: {api_secret[:10]}..." if len(api_secret) > 10 else f"[OK] CLOUDINARY_API_SECRET: {api_secret}")
else:
    print("[X] CLOUDINARY_API_SECRET: NOT SET")

# Check database
print("\n" + "-" * 60)
print("Database Check:")
print("-" * 60)

try:
    from myApp.models import MediaAsset
    count = MediaAsset.objects.count()
    print(f"[OK] Database connection: OK")
    print(f"  Total images in database: {count}")
    if count > 0:
        print("\n  Recent images:")
        for img in MediaAsset.objects.all()[:5]:
            print(f"    - {img.title} (ID: {img.id})")
except Exception as e:
    print(f"[X] Database error: {e}")

# Check Cloudinary import
print("\n" + "-" * 60)
print("Cloudinary Module Check:")
print("-" * 60)

try:
    import cloudinary
    print("[OK] cloudinary module: Installed")
    print(f"  Version: {cloudinary.__version__ if hasattr(cloudinary, '__version__') else 'Unknown'}")
except ImportError:
    print("[X] cloudinary module: NOT INSTALLED")
    print("  Run: pip install cloudinary")

# Summary
print("\n" + "=" * 60)
print("Summary:")
print("=" * 60)

if not cloud_name or not api_key or not api_secret:
    print("\n[!] ISSUE FOUND: Cloudinary credentials are not configured!")
    print("\nTo fix this:")
    print("1. Create a .env file in the project root")
    print("2. Add your Cloudinary credentials:")
    print("   CLOUDINARY_CLOUD_NAME=your_cloud_name")
    print("   CLOUDINARY_API_KEY=your_api_key")
    print("   CLOUDINARY_API_SECRET=your_api_secret")
    print("\n3. Get your credentials from: https://cloudinary.com/console")
    print("4. Restart your Django server after creating .env")
else:
    print("\n[OK] All checks passed! Uploads should work.")
    print("\nIf uploads still fail, check:")
    print("  - Server console for error messages")
    print("  - Browser console (F12) for JavaScript errors")
    print("  - Network tab to see the upload request/response")

print("\n" + "=" * 60)

