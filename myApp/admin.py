from django.contrib import admin
from .models import (
    MediaAsset, SEO, Navigation, Hero, About, Stat, Service, ServicesSection,
    Portfolio, PortfolioProject, Testimonial, FAQ, FAQSection, Contact,
    ContactInfo, ContactFormField, SocialLink, Footer
)


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ['title', 'folder', 'width', 'height', 'file_size', 'created_at']
    list_filter = ['folder', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['original_url', 'web_url', 'thumbnail_url', 'cloudinary_public_id', 'width', 'height', 'file_size', 'created_at', 'updated_at']


@admin.register(SEO)
class SEOAdmin(admin.ModelAdmin):
    list_display = ['page_title', 'updated_at']
    readonly_fields = ['updated_at']


@admin.register(Navigation)
class NavigationAdmin(admin.ModelAdmin):
    list_display = ['label', 'url', 'order', 'is_external', 'is_active']
    list_filter = ['is_active', 'is_external']
    search_fields = ['label', 'url']
    ordering = ['order', 'id']


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle', 'description']
    readonly_fields = ['updated_at']


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle', 'description']
    readonly_fields = ['updated_at']


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'sort_order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['label', 'value']
    ordering = ['sort_order', 'id']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'sort_order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['sort_order', 'id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ServicesSection)
class ServicesSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle']
    readonly_fields = ['updated_at']


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle']
    readonly_fields = ['updated_at']


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'sort_order', 'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = ['title', 'description', 'category']
    ordering = ['sort_order', 'id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'rating', 'sort_order', 'is_active', 'created_at']
    list_filter = ['is_active', 'rating', 'created_at']
    search_fields = ['name', 'company', 'content']
    ordering = ['sort_order', 'id']
    readonly_fields = ['created_at']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'sort_order', 'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = ['question', 'answer']
    ordering = ['sort_order', 'id']
    readonly_fields = ['created_at']


@admin.register(FAQSection)
class FAQSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle']
    readonly_fields = ['updated_at']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle']
    readonly_fields = ['updated_at']


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['label', 'type', 'value', 'sort_order', 'is_active']
    list_filter = ['type', 'is_active']
    search_fields = ['label', 'value']
    ordering = ['sort_order', 'id']
    readonly_fields = ['created_at']


@admin.register(ContactFormField)
class ContactFormFieldAdmin(admin.ModelAdmin):
    list_display = ['label', 'field_type', 'is_required', 'sort_order', 'is_active']
    list_filter = ['field_type', 'is_required', 'is_active']
    search_fields = ['label', 'placeholder']
    ordering = ['sort_order', 'id']
    readonly_fields = ['created_at']


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['label', 'platform', 'url', 'sort_order', 'is_active']
    list_filter = ['platform', 'is_active']
    search_fields = ['label', 'url']
    ordering = ['sort_order', 'id']
    readonly_fields = ['created_at']


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ['copyright_text', 'is_active', 'updated_at']
    list_filter = ['is_active']
    readonly_fields = ['updated_at']
