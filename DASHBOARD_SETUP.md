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
```

**Important:** Add `.env` to `.gitignore` to keep your credentials secure!

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
3. Select an image file
4. Add title and description (optional)
5. Click **Upload**

Images are automatically:
- Compressed if over 10MB
- Converted to WebP format
- Optimized for web delivery
- Stored in Cloudinary CDN

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

1. Check your `.env` file has correct Cloudinary credentials
2. Verify Cloudinary account is active
3. Check file size (max 10MB, auto-compressed if larger)

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



