"""
Cloudinary utility functions for image upload and optimization
"""
import io
from PIL import Image
import cloudinary
import cloudinary.uploader
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Compression settings
MAX_BYTES = 10 * 1024 * 1024  # 10MB
TARGET_BYTES = int(MAX_BYTES * 0.93)  # 9.3MB target after compression


def smart_compress_to_bytes(image_file, target_bytes=TARGET_BYTES, max_quality=85, min_quality=20):
    """
    Compress an image to target size while maintaining quality.
    
    Args:
        image_file: File-like object or PIL Image
        target_bytes: Target file size in bytes
        max_quality: Maximum quality (1-100)
        min_quality: Minimum quality (1-100)
    
    Returns:
        BytesIO object with compressed image
    """
    # Open image
    if isinstance(image_file, Image.Image):
        img = image_file
    else:
        img = Image.open(image_file)
        # Convert RGBA to RGB if necessary (for JPEG compatibility)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
    
    # Determine format
    output_format = 'JPEG' if img.mode == 'RGB' else 'PNG'
    
    # Binary search for optimal quality
    quality = max_quality
    low_quality = min_quality
    high_quality = max_quality
    best_output = None
    
    while low_quality <= high_quality:
        quality = (low_quality + high_quality) // 2
        
        # Compress to bytes
        output = io.BytesIO()
        if output_format == 'JPEG':
            img.save(output, format='JPEG', quality=quality, optimize=True)
        else:
            img.save(output, format='PNG', optimize=True)
        
        size = output.tell()
        
        # Check if we're close enough to target
        if abs(size - target_bytes) < target_bytes * 0.1:  # Within 10% of target
            best_output = output
            break
        
        if size > target_bytes:
            # Too large, reduce quality
            high_quality = quality - 1
            best_output = output
        else:
            # Too small, increase quality
            low_quality = quality + 1
            if best_output is None or size > best_output.tell():
                best_output = output
    
    # Reset to beginning
    if best_output:
        best_output.seek(0)
        return best_output
    
    # Fallback: return original compressed
    output = io.BytesIO()
    if output_format == 'JPEG':
        img.save(output, format='JPEG', quality=max_quality, optimize=True)
    else:
        img.save(output, format='PNG', optimize=True)
    output.seek(0)
    return output


def upload_to_cloudinary(image_file, folder='uploads', public_id=None, overwrite=False):
    """
    Upload an image to Cloudinary with smart compression.
    
    Args:
        image_file: File-like object or InMemoryUploadedFile
        folder: Cloudinary folder path
        public_id: Custom public ID (optional)
        overwrite: Whether to overwrite existing image
    
    Returns:
        dict with upload result containing:
        - original_url: Original image URL
        - web_url: Web-optimized URL (WebP, quality 80, max width 1920)
        - thumbnail_url: Thumbnail URL (WebP, quality 70, width 300)
        - public_id: Cloudinary public ID
        - width: Image width
        - height: Image height
        - bytes: File size
    """
    try:
        # Read image file
        if hasattr(image_file, 'read'):
            image_file.seek(0)
            img_data = image_file.read()
        else:
            img_data = image_file
        
        # Check file size
        file_size = len(img_data) if isinstance(img_data, bytes) else image_file.size
        
        # Compress if needed
        if file_size > MAX_BYTES:
            img = Image.open(io.BytesIO(img_data))
            compressed = smart_compress_to_bytes(img)
            img_data = compressed.read()
            file_size = len(img_data)
        
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            img_data,
            folder=folder,
            public_id=public_id,
            overwrite=overwrite,
            resource_type='image',
            format='auto',  # Auto format (WebP when supported)
        )
        
        # Get image dimensions
        width = upload_result.get('width', 0)
        height = upload_result.get('height', 0)
        public_id = upload_result.get('public_id', '')
        secure_url = upload_result.get('secure_url', '')
        
        # Generate URL variants
        # Web-optimized: WebP, quality 80, max width 1920
        web_url = secure_url.replace(
            '/upload/',
            '/upload/f_webp,q_80,w_1920,c_limit/'
        )
        
        # Thumbnail: WebP, quality 70, width 300
        thumbnail_url = secure_url.replace(
            '/upload/',
            '/upload/f_webp,q_70,w_300,c_limit/'
        )
        
        return {
            'original_url': secure_url,
            'web_url': web_url,
            'thumbnail_url': thumbnail_url,
            'public_id': public_id,
            'width': width,
            'height': height,
            'bytes': file_size,
            'format': upload_result.get('format', ''),
        }
    
    except Exception as e:
        raise Exception(f"Error uploading to Cloudinary: {str(e)}")


def get_cloudinary_url(public_id, transformation=None):
    """
    Generate a Cloudinary URL with optional transformations.
    
    Args:
        public_id: Cloudinary public ID
        transformation: Transformation string (e.g., 'w_800,h_600,c_fill')
    
    Returns:
        Secure URL string
    """
    try:
        if transformation:
            url = cloudinary.CloudinaryImage(public_id).build_url(transformation=transformation)
        else:
            url = cloudinary.CloudinaryImage(public_id).build_url()
        return url
    except Exception as e:
        raise Exception(f"Error generating Cloudinary URL: {str(e)}")


