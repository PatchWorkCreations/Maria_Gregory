# Dashboard System Setup Guide

## Quick Start

### 1. Install Dependencies

All required packages are already in `requirements.txt`. If you need to install them:

```bash
pip install -r requirements.txt
```

### 2. Set Up Cloudinary

1. Sign up for a free account at [cloudinary.com](https://cloudinary.com)
2. Get your credentials from the dashboard:
   - Cloud Name
   - API Key
   - API Secret

3. Create a `.env` file in the project root:

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
OPENAI_API_KEY=your_openai_api_key
```

**Note:** Get your OpenAI API key from [platform.openai.com](https://platform.openai.com/api-keys)

**Important:** Add `.env` to `.gitignore` to keep your credentials secure!

**Quick Setup Helper:**
After creating your `.env` file, verify it's configured correctly:
```bash
python check_upload_setup.py
```

This diagnostic script will check if all required credentials are set up properly.

### 3. Run Migrations

Create the database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

Create an admin account to access the dashboard:

```bash
python manage.py createsuperuser
```

### 5. Start the Server

```bash
python manage.py runserver
```

### 6. Access the Dashboard

Navigate to: `http://localhost:8000/dashboard/`

Login with your superuser credentials.

## Dashboard Features

### ✅ Image Gallery
- Upload images to Cloudinary
- Automatic image optimization
- WebP conversion
- Multiple URL variants (original, web-optimized, thumbnail)

### ✅ Content Management
- SEO settings
- Navigation menu
- Hero section
- About section
- Statistics
- Services
- Portfolio projects
- Testimonials
- FAQs
- Contact information
- Social links
- Footer

### ✅ Features
- WordPress-like CMS (no code changes needed)
- Database-driven content
- Beautiful responsive admin interface
- Secure authentication
- Cloudinary CDN for fast image delivery

## Using the Dashboard

### Upload Images

1. Go to **Gallery** in the sidebar
2. Click **Upload Image**
3. Select one or multiple image files (hold Ctrl/Cmd to select multiple)
4. Add title and description (optional - applies to first image only)
5. Click **Upload**

**Features:**
- ✅ Upload multiple images at once
- ✅ See selected files before uploading
- ✅ Progress tracking for batch uploads
- ✅ Automatic compression if over 10MB
- ✅ Converted to WebP format
- ✅ Optimized for web delivery
- ✅ Stored in Cloudinary CDN

### Edit Content

1. Navigate to any section in the sidebar (e.g., Hero, About, SEO)
2. Fill in the form fields
3. Click **Save Changes**

Changes are immediately reflected on your website!

### Copy Image URLs

1. Go to **Gallery**
2. Hover over any image
3. Click **Copy URL**
4. Paste the URL in any content field

## Find and Retrieve Images

### Method 1: Using the Dashboard Gallery

1. Go to **Gallery** in the dashboard sidebar
2. Browse through all uploaded images
3. Hover over an image to copy its URL

### Method 2: Find Image by Cloudinary Public ID

If you have a Cloudinary public ID (like `dkkwbqr8e`), you can find the image:

```bash
python manage.py get_image --public-id dkkwbqr8e
```

This will show:
- Image title and description
- All URL variants (original, web-optimized, thumbnail)
- Image dimensions and file size
- Database ID and creation date

**Get only the URL:**
```bash
python manage.py get_image --public-id dkkwbqr8e --url-only
```

### Method 3: Search Images by Title or Description

Search for images in the database:

```bash
python manage.py get_image --search "hero"
```

This will find all images with "hero" in the title or description.

### Method 4: List All Images

View all images in the database:

```bash
python manage.py get_image --list-all
```

### Method 5: Generate URL from Public ID (Even if Not in Database)

If you have a Cloudinary public ID but the image isn't in your database yet, you can still generate its URL using the utility function:

```python
from myApp.utils.cloudinary_utils import get_cloudinary_url

url = get_cloudinary_url('dkkwbqr8e')
# Returns: https://res.cloudinary.com/your-cloud/image/upload/dkkwbqr8e

# With transformations
url = get_cloudinary_url('dkkwbqr8e', transformation={'width': 800, 'height': 600})
```

### Where Images Are Stored

Images are stored in two places:

1. **Cloudinary CDN** - All image files are stored in your Cloudinary account
2. **Database (MediaAsset model)** - Metadata, URLs, and references are stored locally

The `cloudinary_public_id` field in the database links to the actual file in Cloudinary.

## Manually Import Images from Folder

If you have multiple images in a folder that you want to import to Cloudinary, you can use the management command to bulk import them:

### Basic Usage

Import all images from a folder:

```bash
python manage.py import_images --folder path/to/your/images/
```

### Options

**Import to a specific Cloudinary folder:**
```bash
python manage.py import_images --folder path/to/images/ --cloudinary-folder myApp/portfolio
```

**Import recursively from subdirectories:**
```bash
python manage.py import_images --folder path/to/images/ --recursive
```

**Specify image file extensions:**
```bash
python manage.py import_images --folder path/to/images/ --extensions jpg,png,webp
```

### Examples

**Windows:**
```bash
python manage.py import_images --folder "C:\Users\YourName\Pictures\website-images"
```

**Mac/Linux:**
```bash
python manage.py import_images --folder ~/Pictures/website-images
```

**Import from current directory:**
```bash
python manage.py import_images --folder ./images
```

### Supported Image Formats

By default, the command supports:
- JPG/JPEG
- PNG
- GIF
- WebP
- BMP
- SVG

### What Happens During Import

1. ✅ Images are automatically compressed if over 10MB
2. ✅ Images are optimized and converted to WebP format
3. ✅ Multiple URL variants are created (original, web-optimized, thumbnail)
4. ✅ Images are stored in Cloudinary CDN
5. ✅ Image metadata is saved to the database
6. ✅ Duplicate images (by filename) are automatically skipped

### Tips

- **Organize your images first**: Create folders for different image types (e.g., `hero-images/`, `portfolio/`, `testimonials/`)
- **Use descriptive filenames**: The filename (without extension) becomes the image title
- **Check file sizes**: Very large images will be compressed automatically
- **Verify Cloudinary credentials**: Make sure your `.env` file has the correct Cloudinary credentials before importing

## Import Existing Data

If you have existing JSON data, you can import it:

```bash
python manage.py import_homepage_data --file path/to/data.json
```

Or create default data structure:

```bash
python manage.py import_homepage_data
```

## Template Usage

Your homepage template can access content from the database:

```django
{% if content.hero %}
    <h1>{{ content.hero.title }}</h1>
    <p>{{ content.hero.description }}</p>
{% endif %}

{% if content.navigation %}
    {% for item in content.navigation %}
        <a href="{{ item.url }}">{{ item.label }}</a>
    {% endfor %}
{% endif %}
```

## Troubleshooting

### Images Not Uploading

**Most Common Issue: Missing `.env` file**

If uploads aren't working, the most likely cause is a missing or incorrectly configured `.env` file.

**Quick Diagnostic:**
```bash
python check_upload_setup.py
```

This will check:
- If `.env` file exists
- If Cloudinary credentials are set
- If database is accessible
- If Cloudinary module is installed

**Fix Steps:**
1. **Check if `.env` file exists** in the project root
2. **Verify it contains:**
   ```
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```
3. **Get credentials from:** https://cloudinary.com/console
4. **Restart Django server** after creating/updating `.env`

**Other Issues:**
- Check your `.env` file has correct Cloudinary credentials
- Verify Cloudinary account is active
- Check file size (max 10MB, auto-compressed if larger)
- Check browser console (F12) for JavaScript errors
- Check server console for Python errors

### Can't Login

1. Make sure you created a superuser: `python manage.py createsuperuser`
2. Verify user is active in Django admin
3. Check you're using correct username/password

### Database Errors

1. Run migrations: `python manage.py makemigrations && python manage.py migrate`
2. Check database connection in `settings.py`

## Next Steps

1. ✅ Set up Cloudinary account
2. ✅ Create `.env` file with credentials
3. ✅ Run migrations
4. ✅ Create superuser
5. ✅ Start uploading images
6. ✅ Edit your content sections
7. ✅ Customize templates as needed

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Django/Cloudinary documentation
3. Check error logs in the console

---

**Happy Content Managing! 🚀**



