from django.db import models
from django.utils.text import slugify
from django.core.validators import URLValidator
import json

# Use JSONField - available in Django 3.1+
JSONField = models.JSONField


class MediaAsset(models.Model):
    """Cloudinary image assets - stores only URLs, no file storage"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    original_url = models.URLField(max_length=500)
    web_url = models.URLField(max_length=500, blank=True)  # Web-optimized version
    thumbnail_url = models.URLField(max_length=500, blank=True)  # Thumbnail version
    cloudinary_public_id = models.CharField(max_length=200, blank=True)
    folder = models.CharField(max_length=200, default='uploads')
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    file_size = models.IntegerField(null=True, blank=True)  # in bytes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SEO(models.Model):
    """SEO metadata for the homepage"""
    page_title = models.CharField(max_length=200, default='Home')
    meta_description = models.TextField(max_length=500, blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    og_title = models.CharField(max_length=200, blank=True)
    og_description = models.TextField(max_length=500, blank=True)
    og_image = models.URLField(max_length=500, blank=True)
    twitter_card = models.CharField(max_length=50, default='summary_large_image', blank=True)
    canonical_url = models.URLField(max_length=500, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SEO"
        verbose_name_plural = "SEO"

    def __str__(self):
        return f"SEO - {self.page_title}"


class Navigation(models.Model):
    """Navigation menu items"""
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    is_external = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name_plural = "Navigation Items"

    def __str__(self):
        return self.label


class Hero(models.Model):
    """Hero section content"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    button_text = models.CharField(max_length=100, blank=True)
    button_url = models.CharField(max_length=200, blank=True)
    background_image_url = models.URLField(max_length=500, blank=True)
    content = JSONField(default=dict, blank=True)  # Flexible JSON storage
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hero Sections"

    def __str__(self):
        return self.title


class About(models.Model):
    """About section content"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    quote = models.TextField(blank=True)
    content = JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "About Sections"

    def __str__(self):
        return self.title


class Stat(models.Model):
    """Statistics/numbers to display"""
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)  # Can be number or text
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)  # Font Awesome icon class
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = "Statistic"
        verbose_name_plural = "Statistics"

    def __str__(self):
        return f"{self.label}: {self.value}"


class Service(models.Model):
    """Services offered"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    content = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.title


class ServicesSection(models.Model):
    """Services section header/content"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    content = JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Services Section"
        verbose_name_plural = "Services Sections"

    def __str__(self):
        return self.title


class Portfolio(models.Model):
    """Portfolio section header/content"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    content = JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Portfolio Sections"

    def __str__(self):
        return self.title


class PortfolioProject(models.Model):
    """Individual portfolio projects"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    project_url = models.URLField(max_length=500, blank=True)
    category = models.CharField(max_length=100, blank=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    content = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """Customer testimonials"""
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    image_url = models.URLField(max_length=500, blank=True)
    rating = models.IntegerField(default=5, blank=True, null=True)  # 1-5 stars
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f"{self.name} - {self.company}"


class FAQ(models.Model):
    """Frequently Asked Questions"""
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question[:50]


class FAQSection(models.Model):
    """FAQ section header/content"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    content = JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FAQ Section"
        verbose_name_plural = "FAQ Sections"

    def __str__(self):
        return self.title


class Contact(models.Model):
    """Contact section header/content"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    content = JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Contact Sections"

    def __str__(self):
        return self.title


class ContactInfo(models.Model):
    """Contact information (email, phone, address, etc.)"""
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('address', 'Address'),
        ('hours', 'Business Hours'),
        ('other', 'Other'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='other')
    label = models.CharField(max_length=200)
    value = models.CharField(max_length=500)
    icon = models.CharField(max_length=100, blank=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"

    def __str__(self):
        return f"{self.label}: {self.value}"


class ContactFormField(models.Model):
    """Contact form fields"""
    FIELD_TYPE_CHOICES = [
        ('text', 'Text'),
        ('email', 'Email'),
        ('textarea', 'Textarea'),
        ('select', 'Select'),
        ('checkbox', 'Checkbox'),
    ]
    label = models.CharField(max_length=200)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES, default='text')
    placeholder = models.CharField(max_length=200, blank=True)
    is_required = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    options = JSONField(default=list, blank=True)  # For select/checkbox options
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = "Contact Form Field"
        verbose_name_plural = "Contact Form Fields"

    def __str__(self):
        return self.label


class SocialLink(models.Model):
    """Social media links"""
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('pinterest', 'Pinterest'),
        ('other', 'Other'),
    ]
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, default='other')
    label = models.CharField(max_length=200)
    url = models.URLField(max_length=500)
    icon = models.CharField(max_length=100, blank=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return f"{self.platform}: {self.label}"


class Footer(models.Model):
    """Footer content"""
    copyright_text = models.CharField(max_length=200, default='© 2025 All rights reserved.')
    content = JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Footer"

    def __str__(self):
        return "Footer"


class DecadesSection(models.Model):
    """Decades of Walking With Leaders section header/content"""
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    description = models.TextField(blank=True)
    closing_quote = models.TextField(blank=True)
    content = JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Decades Section"
        verbose_name_plural = "Decades Sections"

    def __str__(self):
        return self.title


class DecadesTimelineItem(models.Model):
    """Individual timeline items for Decades of Walking With Leaders section"""
    section = models.ForeignKey(DecadesSection, on_delete=models.CASCADE, related_name='timeline_items', null=True, blank=True)
    period = models.CharField(max_length=100, blank=True)  # e.g., "2009–Present"
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    reflection = models.TextField(blank=True)  # Reflection question/quote
    image_url = models.URLField(max_length=500, blank=True)
    icon = models.CharField(max_length=100, blank=True)  # Font Awesome icon class
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = "Decades Timeline Item"
        verbose_name_plural = "Decades Timeline Items"

    def __str__(self):
        return f"{self.period} - {self.title}"


class LionSection(models.Model):
    """The Lion You Don't See section content"""
    title = models.CharField(max_length=200, default="The Lion You Don't See")
    icon = models.CharField(max_length=100, default='fas fa-star', blank=True)  # Font Awesome icon class
    intro_text = models.TextField(blank=True)  # First paragraph
    paragraph_1 = models.TextField(blank=True)  # Second paragraph
    paragraph_2 = models.TextField(blank=True)  # Third paragraph
    reflection_question = models.TextField(blank=True)  # Reflection question
    background_image_url = models.URLField(max_length=500, blank=True)  # Background image
    book_cover_image_url = models.URLField(max_length=500, blank=True)  # Book cover image
    closing_quote = models.TextField(blank=True)  # Quote below book
    content = JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lion Section"
        verbose_name_plural = "Lion Sections"

    def __str__(self):
        return self.title