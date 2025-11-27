"""
Management command to import homepage data from JSON file
Usage: python manage.py import_homepage_data [--file path/to/data.json]
"""
from django.core.management.base import BaseCommand
from django.db import transaction
import json
import os

from myApp.models import (
    SEO, Navigation, Hero, About, Stat, Service, ServicesSection,
    Portfolio, PortfolioProject, Testimonial, FAQ, FAQSection, Contact,
    ContactInfo, ContactFormField, SocialLink, Footer
)


class Command(BaseCommand):
    help = 'Import homepage data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to JSON file (optional)',
            default=None,
        )

    def handle(self, *args, **options):
        file_path = options.get('file')
        
        if not file_path:
            self.stdout.write(self.style.WARNING('No file specified. Creating default data structure.'))
            self.create_default_data()
            return
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            with transaction.atomic():
                self.import_data(data)
            
            self.stdout.write(self.style.SUCCESS('Successfully imported homepage data!'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {str(e)}'))

    def create_default_data(self):
        """Create default data structure if no file is provided"""
        with transaction.atomic():
            # Create default SEO
            SEO.objects.get_or_create(
                pk=1,
                defaults={
                    'page_title': 'Home',
                    'meta_description': 'Welcome to our website',
                }
            )
            
            # Create default Hero
            Hero.objects.get_or_create(
                pk=1,
                defaults={
                    'title': 'Welcome',
                    'subtitle': 'Your subtitle here',
                    'description': 'Your description here',
                    'is_active': True,
                }
            )
            
            # Create default Footer
            Footer.objects.get_or_create(
                pk=1,
                defaults={
                    'copyright_text': '© 2025 All rights reserved.',
                    'is_active': True,
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Created default data structure!'))

    def import_data(self, data):
        """Import data from JSON structure"""
        # SEO
        if 'seo' in data:
            seo_data = data['seo']
            SEO.objects.update_or_create(
                pk=1,
                defaults=seo_data
            )
        
        # Navigation
        if 'navigation' in data:
            Navigation.objects.all().delete()
            for item in data['navigation']:
                Navigation.objects.create(**item)
        
        # Hero
        if 'hero' in data:
            Hero.objects.update_or_create(
                pk=1,
                defaults=data['hero']
            )
        
        # About
        if 'about' in data:
            About.objects.update_or_create(
                pk=1,
                defaults=data['about']
            )
        
        # Stats
        if 'stats' in data:
            Stat.objects.all().delete()
            for stat in data['stats']:
                Stat.objects.create(**stat)
        
        # Services Section
        if 'services_section' in data:
            ServicesSection.objects.update_or_create(
                pk=1,
                defaults=data['services_section']
            )
        
        # Services
        if 'services' in data:
            Service.objects.all().delete()
            for service in data['services']:
                Service.objects.create(**service)
        
        # Portfolio
        if 'portfolio' in data:
            Portfolio.objects.update_or_create(
                pk=1,
                defaults=data['portfolio']
            )
        
        # Portfolio Projects
        if 'portfolio_projects' in data:
            PortfolioProject.objects.all().delete()
            for project in data['portfolio_projects']:
                PortfolioProject.objects.create(**project)
        
        # Testimonials
        if 'testimonials' in data:
            Testimonial.objects.all().delete()
            for testimonial in data['testimonials']:
                Testimonial.objects.create(**testimonial)
        
        # FAQ Section
        if 'faq_section' in data:
            FAQSection.objects.update_or_create(
                pk=1,
                defaults=data['faq_section']
            )
        
        # FAQs
        if 'faqs' in data:
            FAQ.objects.all().delete()
            for faq in data['faqs']:
                FAQ.objects.create(**faq)
        
        # Contact
        if 'contact' in data:
            Contact.objects.update_or_create(
                pk=1,
                defaults=data['contact']
            )
        
        # Contact Info
        if 'contact_info' in data:
            ContactInfo.objects.all().delete()
            for info in data['contact_info']:
                ContactInfo.objects.create(**info)
        
        # Contact Form Fields
        if 'contact_form_fields' in data:
            ContactFormField.objects.all().delete()
            for field in data['contact_form_fields']:
                ContactFormField.objects.create(**field)
        
        # Social Links
        if 'social_links' in data:
            SocialLink.objects.all().delete()
            for link in data['social_links']:
                SocialLink.objects.create(**link)
        
        # Footer
        if 'footer' in data:
            Footer.objects.update_or_create(
                pk=1,
                defaults=data['footer']
            )


