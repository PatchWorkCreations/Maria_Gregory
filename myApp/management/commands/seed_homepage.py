"""
Management command to seed the database with initial homepage content
Run with: python manage.py seed_homepage
"""
from django.core.management.base import BaseCommand
from myApp.models import (
    SEO, Navigation, Hero, About, Stat, Service, ServicesSection,
    Portfolio, PortfolioProject, Testimonial, FAQ, FAQSection, Contact,
    ContactInfo, ContactFormField, SocialLink, Footer
)


class Command(BaseCommand):
    help = 'Seeds the database with initial homepage content'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed homepage content...'))
        
        # 1. SEO
        seo, created = SEO.objects.get_or_create(pk=1)
        seo.page_title = "Maria Gregory – Someone Leaders Can Lean On"
        seo.meta_description = "Maria Gregory offers quiet, private 1:1 support for founders, mentors, executives, and high-responsibility leaders — especially the ones who are used to figuring things out on their own."
        seo.meta_keywords = "leadership mentor, executive coaching, founder support, leadership guidance, Maria Gregory"
        seo.og_title = "Maria Gregory – Someone Leaders Can Lean On"
        seo.og_description = "A private, steady space for the people who carry everyone else."
        seo.og_image = "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1200&h=630&fit=crop&q=80"
        seo.twitter_card = "summary_large_image"
        seo.canonical_url = ""
        seo.save()
        self.stdout.write(self.style.SUCCESS('✓ SEO settings created'))
        
        # 2. Navigation
        Navigation.objects.all().delete()
        nav_items = [
            {'label': 'Home', 'url': '/', 'order': 1, 'is_external': False},
            {'label': 'About', 'url': '#about', 'order': 2, 'is_external': False},
            {'label': 'Mentorship', 'url': '#mentorship', 'order': 3, 'is_external': False},
            {'label': 'Contact', 'url': '#contact', 'order': 4, 'is_external': False},
        ]
        for item in nav_items:
            Navigation.objects.create(**item)
        self.stdout.write(self.style.SUCCESS('✓ Navigation items created'))
        
        # 3. Hero Section
        hero, created = Hero.objects.get_or_create(pk=1)
        hero.title = "Maria Gregory"
        hero.subtitle = "Someone Leaders Can Lean On."
        hero.description = '"I\'m the person leaders turn to when they\'ve carried things far on their own and simply want a steadier place to think, breathe, and be human again."'
        hero.button_text = "Start a Conversation"
        hero.button_url = "#contact"
        hero.background_image_url = "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1920&h=1080&fit=crop&q=80"
        hero.is_active = True
        hero.save()
        self.stdout.write(self.style.SUCCESS('✓ Hero section created'))
        
        # 4. About Section
        about, created = About.objects.get_or_create(pk=1)
        about.title = "The Human Behind the Work"
        about.subtitle = "The roles that keep me grounded."
        about.description = '"Before I\'m anyone\'s mentor, I\'m a human being in real relationships, with real people who see me on my good days and my undone days."'
        about.image_url = "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=800&h=800&fit=crop&q=80"
        about.quote = "If you're often the one others rely on, notice what it feels like to land somewhere you don't have to hold anything just yet."
        about.is_active = True
        about.save()
        self.stdout.write(self.style.SUCCESS('✓ About section created'))
        
        # 5. Statistics
        Stat.objects.all().delete()
        stats = [
            {'label': 'Years Mentoring', 'value': '15+', 'description': 'Supporting leaders', 'icon': 'fas fa-calendar-alt', 'sort_order': 1},
            {'label': 'Leaders Supported', 'value': '500+', 'description': 'Founders, executives, coaches', 'icon': 'fas fa-users', 'sort_order': 2},
            {'label': '1:1 Sessions', 'value': '2000+', 'description': 'Private guidance sessions', 'icon': 'fas fa-handshake', 'sort_order': 3},
        ]
        for stat in stats:
            Stat.objects.create(**stat)
        self.stdout.write(self.style.SUCCESS('✓ Statistics created'))
        
        # 6. Services Section
        services_section, created = ServicesSection.objects.get_or_create(pk=1)
        services_section.title = "1:1 Work With Me"
        services_section.subtitle = "A private, steady space for the people who carry everyone else."
        services_section.description = "This is a quiet, confidential space for leaders who rarely get to set their armor down."
        services_section.is_active = True
        services_section.save()
        self.stdout.write(self.style.SUCCESS('✓ Services section created'))
        
        # 7. Services
        Service.objects.all().delete()
        services = [
            {
                'title': 'Clarity & Alignment Sessions',
                'description': 'We peel back the noise so you can reconnect to why you lead and where you\'re truly going.',
                'icon': 'fas fa-compass',
                'image_url': '',
                'sort_order': 1
            },
            {
                'title': 'Emotional & Spiritual Grounding',
                'description': 'You get a steady space to process what you\'re holding — emotionally, spiritually, mentally — without needing to be "on."',
                'icon': 'fas fa-seedling',
                'image_url': '',
                'sort_order': 2
            },
            {
                'title': 'Strategic Leadership Support',
                'description': 'When the decisions are heavy and the path forward isn\'t clear, we create space to think clearly.',
                'icon': 'fas fa-chess',
                'image_url': '',
                'sort_order': 3
            },
        ]
        for service in services:
            Service.objects.create(**service)
        self.stdout.write(self.style.SUCCESS('✓ Services created'))
        
        # 8. Portfolio Section (optional - can be used for case studies)
        portfolio, created = Portfolio.objects.get_or_create(pk=1)
        portfolio.title = "Patterns I See Over and Over"
        portfolio.subtitle = "If you see yourself in more than one, that's often where the deepest work begins."
        portfolio.description = ""
        portfolio.is_active = True
        portfolio.save()
        self.stdout.write(self.style.SUCCESS('✓ Portfolio section created'))
        
        # 9. Portfolio Projects (Leader Types)
        PortfolioProject.objects.all().delete()
        projects = [
            {
                'title': 'Founders & CEOs',
                'description': 'You built something from nothing. Now you\'re carrying the weight of everyone who depends on it — and sometimes, you wonder who\'s carrying you.',
                'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop&q=80',
                'project_url': '',
                'category': 'Leader Type',
                'sort_order': 1
            },
            {
                'title': 'Coaches & Mentors',
                'description': 'You hold space for others constantly. But where do you go when you need someone to hold space for you?',
                'image_url': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=600&h=400&fit=crop&q=80',
                'project_url': '',
                'category': 'Leader Type',
                'sort_order': 2
            },
            {
                'title': 'High-Responsibility Leaders',
                'description': 'You\'re the one people turn to. The steady one. The one who figures it out. But who do you turn to?',
                'image_url': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&h=400&fit=crop&q=80',
                'project_url': '',
                'category': 'Leader Type',
                'sort_order': 3
            },
        ]
        for project in projects:
            PortfolioProject.objects.create(**project)
        self.stdout.write(self.style.SUCCESS('✓ Portfolio projects created'))
        
        # 10. Testimonials
        Testimonial.objects.all().delete()
        testimonials = [
            {
                'name': 'Sarah Chen',
                'role': 'Founder & CEO',
                'company': 'Tech Startup',
                'content': 'Maria created a space where I could finally set my armor down. For the first time in years, I felt like I didn\'t have to be impressive — I could just be human.',
                'image_url': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200&h=200&fit=crop&q=80',
                'rating': 5,
                'sort_order': 1
            },
            {
                'name': 'Michael Rodriguez',
                'role': 'Executive Coach',
                'company': 'Leadership Consulting',
                'content': 'As someone who coaches others, I needed someone who could see me — not just my role. Maria does that with profound grace and wisdom.',
                'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop&q=80',
                'rating': 5,
                'sort_order': 2
            },
            {
                'name': 'Jennifer Park',
                'role': 'VP of Operations',
                'company': 'Fortune 500',
                'content': 'The clarity sessions with Maria helped me reconnect to why I lead. I\'m moving toward a life I actually chose, not one that just happened.',
                'image_url': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=200&h=200&fit=crop&q=80',
                'rating': 5,
                'sort_order': 3
            },
        ]
        for testimonial in testimonials:
            Testimonial.objects.create(**testimonial)
        self.stdout.write(self.style.SUCCESS('✓ Testimonials created'))
        
        # 11. FAQ Section
        faq_section, created = FAQSection.objects.get_or_create(pk=1)
        faq_section.title = "Questions Leaders Often Ask"
        faq_section.subtitle = "Common questions about working with me"
        faq_section.description = ""
        faq_section.is_active = True
        faq_section.save()
        self.stdout.write(self.style.SUCCESS('✓ FAQ section created'))
        
        # 12. FAQs
        FAQ.objects.all().delete()
        faqs = [
            {
                'question': 'Do I need to be struggling to reach out?',
                'answer': 'Not at all. Many of the people I mentor simply want a steadier, truer way of living and leading — a space where they can think clearly and be understood without needing to explain themselves.',
                'category': 'General',
                'sort_order': 1
            },
            {
                'question': 'What makes this different from coaching?',
                'answer': 'This isn\'t a performance space or a place where you need to prove anything. You don\'t need fixing — you just deserve a steadier place to land. It\'s mentorship, not coaching.',
                'category': 'General',
                'sort_order': 2
            },
            {
                'question': 'How do we work together?',
                'answer': 'We work 1:1 in private sessions. The format is flexible — we can meet regularly or as needed. The space is yours to use as you need it.',
                'category': 'Process',
                'sort_order': 3
            },
            {
                'question': 'Is this confidential?',
                'answer': 'Absolutely. This is a private, confidential space. What we discuss stays between us.',
                'category': 'Process',
                'sort_order': 4
            },
        ]
        for faq in faqs:
            FAQ.objects.create(**faq)
        self.stdout.write(self.style.SUCCESS('✓ FAQs created'))
        
        # 13. Contact Section
        contact, created = Contact.objects.get_or_create(pk=1)
        # Call To Action Section (Upper Dark Section)
        contact.cta_title = "Let's start a conversation"
        contact.cta_subtitle = "Ready For Someone In Your Corner?"
        contact.cta_description = "You don't have to be struggling to reach out. Many of the people I mentor simply want a steadier, truer way of living and leading."
        contact.cta_quote = "You don't have to carry all of this alone. Even the strongest leaders deserve a place to lay it all down."
        # CTA Buttons
        contact.cta_button1_text = "Apply for 1:1 Guidance"
        contact.cta_button1_url = "#contact"
        contact.cta_button2_text = "Text Me"
        contact.cta_button2_url = "sms:+17407215817"
        contact.cta_button3_text = "Ask a Question First"
        contact.cta_button3_url = "mailto:contact@mariagregory.com"
        contact.subtitle = "Let's start a conversation"
        contact.title = "Let's start a conversation"
        contact.subtitle = ""
        contact.description = "You don't have to be struggling to reach out. Many of the people I mentor simply want a steadier, truer way of living and leading."
        contact.is_active = True
        contact.save()
        self.stdout.write(self.style.SUCCESS('✓ Contact section created'))
        
        # 14. Contact Info
        ContactInfo.objects.all().delete()
        contact_infos = [
            {'type': 'email', 'label': 'Email', 'value': 'hello@mariagregory.com', 'icon': 'fas fa-envelope', 'sort_order': 1},
            {'type': 'phone', 'label': 'Phone', 'value': '+1 (555) 123-4567', 'icon': 'fas fa-phone', 'sort_order': 2},
            {'type': 'address', 'label': 'Location', 'value': 'Available for remote sessions worldwide', 'icon': 'fas fa-map-marker-alt', 'sort_order': 3},
        ]
        for info in contact_infos:
            ContactInfo.objects.create(**info)
        self.stdout.write(self.style.SUCCESS('✓ Contact info created'))
        
        # 15. Contact Form Fields
        ContactFormField.objects.all().delete()
        form_fields = [
            {'label': 'Name', 'field_type': 'text', 'placeholder': 'Your name', 'is_required': True, 'sort_order': 1},
            {'label': 'Email', 'field_type': 'email', 'placeholder': 'your.email@example.com', 'is_required': True, 'sort_order': 2},
            {'label': 'Message', 'field_type': 'textarea', 'placeholder': 'Tell me what brings you here...', 'is_required': True, 'sort_order': 3},
        ]
        for field in form_fields:
            ContactFormField.objects.create(**field)
        self.stdout.write(self.style.SUCCESS('✓ Contact form fields created'))
        
        # 16. Social Links
        SocialLink.objects.all().delete()
        social_links = [
            {'platform': 'linkedin', 'label': 'LinkedIn', 'url': 'https://www.linkedin.com/in/maria-gregory-a29a7a69/', 'icon': 'fab fa-linkedin', 'sort_order': 1},
         
        ]
        for link in social_links:
            SocialLink.objects.create(**link)
        self.stdout.write(self.style.SUCCESS('✓ Social links created'))
        
        # 17. Footer
        footer, created = Footer.objects.get_or_create(pk=1)
        footer.copyright_text = "© 2025 Maria Gregory. All rights reserved."
        footer.is_active = True
        footer.save()
        self.stdout.write(self.style.SUCCESS('✓ Footer created'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Homepage content seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('You can now manage all content through the dashboard at /dashboard/'))


