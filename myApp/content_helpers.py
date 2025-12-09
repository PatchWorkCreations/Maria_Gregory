"""
Content helpers - Convert database models to JSON format for templates
"""
from .models import (
    MediaAsset, SEO, Navigation, Hero, About, Stat, Service, ServicesSection,
    Portfolio, PortfolioProject, Testimonial, FAQ, FAQSection, Contact,
    ContactInfo, ContactFormField, SocialLink, Footer, DecadesSection, DecadesTimelineItem,
    LionSection
)


def get_homepage_content_from_db():
    """
    Convert database models to JSON format for homepage template.
    Returns a dictionary matching the structure expected by templates.
    """
    content = {}
    
    # SEO
    try:
        seo = SEO.objects.first()
        if seo:
            content['seo'] = {
                'page_title': seo.page_title,
                'meta_description': seo.meta_description,
                'meta_keywords': seo.meta_keywords,
                'og_title': seo.og_title,
                'og_description': seo.og_description,
                'og_image': seo.og_image,
                'twitter_card': seo.twitter_card,
                'canonical_url': seo.canonical_url,
            }
    except:
        content['seo'] = {}
    
    # Navigation
    try:
        nav_items = Navigation.objects.filter(is_active=True).order_by('order', 'id')
        content['navigation'] = [
            {
                'label': item.label,
                'url': item.url,
                'is_external': item.is_external,
            }
            for item in nav_items
        ]
    except:
        content['navigation'] = []
    
    # Hero
    try:
        hero = Hero.objects.filter(is_active=True).first()
        if hero:
            content['hero'] = {
                'title': hero.title,
                'subtitle': hero.subtitle,
                'description': hero.description,
                'button_text': hero.button_text,
                'button_url': hero.button_url,
                'background_image_url': hero.background_image_url,
                **hero.content,  # Merge any additional JSON content
            }
    except:
        content['hero'] = {}
    
    # About
    try:
        about = About.objects.filter(is_active=True).first()
        if about:
            content['about'] = {
                'title': about.title,
                'subtitle': about.subtitle,
                'description': about.description,
                'image_url': about.image_url,
                'quote': about.quote,
                **about.content,
            }
    except:
        content['about'] = {}
    
    # Stats
    try:
        stats = Stat.objects.filter(is_active=True).order_by('sort_order', 'id')
        content['stats'] = [
            {
                'label': stat.label,
                'value': stat.value,
                'description': stat.description,
                'icon': stat.icon,
            }
            for stat in stats
        ]
    except:
        content['stats'] = []
    
    # Services Section
    try:
        services_section = ServicesSection.objects.filter(is_active=True).first()
        if services_section:
            content['services_section'] = {
                'title': services_section.title,
                'subtitle': services_section.subtitle,
                'description': services_section.description,
                **services_section.content,
            }
    except:
        content['services_section'] = {}
    
    # Services
    try:
        services = Service.objects.filter(is_active=True).order_by('sort_order', 'id')
        content['services'] = [
            {
                'title': service.title,
                'description': service.description,
                'icon': service.icon,
                'image_url': service.image_url,
                **service.content,
            }
            for service in services
        ]
    except:
        content['services'] = []
    
    # Portfolio
    try:
        portfolio = Portfolio.objects.filter(is_active=True).first()
        if portfolio:
            content['portfolio'] = {
                'title': portfolio.title,
                'subtitle': portfolio.subtitle,
                'description': portfolio.description,
                **portfolio.content,
            }
    except:
        content['portfolio'] = {}
    
    # Portfolio Projects
    try:
        projects = PortfolioProject.objects.filter(is_active=True).order_by('sort_order', 'id')
        content['portfolio_projects'] = [
            {
                'title': project.title,
                'description': project.description,
                'image_url': project.image_url,
                'project_url': project.project_url,
                'category': project.category,
                **project.content,
            }
            for project in projects
        ]
    except:
        content['portfolio_projects'] = []
    
    # Testimonials
    try:
        testimonials = Testimonial.objects.filter(is_active=True).order_by('sort_order', 'id')
        content['testimonials'] = [
            {
                'name': testimonial.name,
                'role': testimonial.role,
                'company': testimonial.company,
                'content': testimonial.content,
                'image_url': testimonial.image_url,
                'rating': testimonial.rating,
            }
            for testimonial in testimonials
        ]
    except:
        content['testimonials'] = []
    
    # FAQ Section
    try:
        faq_section = FAQSection.objects.filter(is_active=True).first()
        if faq_section:
            content['faq_section'] = {
                'title': faq_section.title,
                'subtitle': faq_section.subtitle,
                'description': faq_section.description,
                **faq_section.content,
            }
    except:
        content['faq_section'] = {}
    
    # FAQs
    try:
        faqs = FAQ.objects.filter(is_active=True).order_by('sort_order', 'id')
        content['faqs'] = [
            {
                'question': faq.question,
                'answer': faq.answer,
                'category': faq.category,
            }
            for faq in faqs
        ]
    except:
        content['faqs'] = []
    
    # Contact
    try:
        contact = Contact.objects.filter(is_active=True).first()
        if contact:
            content['contact'] = {
                'cta_title': contact.cta_title,
                'cta_subtitle': contact.cta_subtitle,
                'cta_description': contact.cta_description,
                'cta_quote': contact.cta_quote,
                'cta_button1_text': contact.cta_button1_text,
                'cta_button1_url': contact.cta_button1_url,
                'cta_button2_text': contact.cta_button2_text,
                'cta_button2_url': contact.cta_button2_url,
                'cta_button3_text': contact.cta_button3_text,
                'cta_button3_url': contact.cta_button3_url,
                'title': contact.title,
                'subtitle': contact.subtitle,
                'description': contact.description,
                **contact.content,
            }
    except:
        content['contact'] = {}
    
    # Contact Info
    try:
        contact_infos = ContactInfo.objects.filter(is_active=True).order_by('sort_order', 'id')
        content['contact_info'] = [
            {
                'type': info.type,
                'label': info.label,
                'value': info.value,
                'icon': info.icon,
            }
            for info in contact_infos
        ]
    except:
        content['contact_info'] = []
    
    # Contact Form Fields
    try:
        form_fields = ContactFormField.objects.filter(is_active=True).order_by('sort_order', 'id')
        content['contact_form_fields'] = [
            {
                'label': field.label,
                'field_type': field.field_type,
                'placeholder': field.placeholder,
                'is_required': field.is_required,
                'options': field.options,
            }
            for field in form_fields
        ]
    except:
        content['contact_form_fields'] = []
    
    # Social Links
    try:
        social_links = SocialLink.objects.filter(is_active=True).order_by('sort_order', 'id')
        content['social_links'] = [
            {
                'platform': link.platform,
                'label': link.label,
                'url': link.url,
                'icon': link.icon,
            }
            for link in social_links
        ]
    except:
        content['social_links'] = []
    
    # Footer
    try:
        footer = Footer.objects.filter(is_active=True).first()
        if footer:
            content['footer'] = {
                'copyright_text': footer.copyright_text,
                **footer.content,
            }
    except:
        content['footer'] = {
            'copyright_text': '© 2025 All rights reserved.'
        }
    
    # Decades Section
    try:
        decades_section = DecadesSection.objects.filter(is_active=True).first()
        if decades_section:
            content['decades_section'] = {
                'title': decades_section.title,
                'subtitle': decades_section.subtitle,
                'description': decades_section.description,
                'closing_quote': decades_section.closing_quote,
                **decades_section.content,
            }
    except:
        content['decades_section'] = {}
    
    # Decades Timeline Items
    try:
        timeline_items = DecadesTimelineItem.objects.filter(is_active=True).order_by('sort_order', 'id')
        content['decades_timeline_items'] = [
            {
                'period': item.period,
                'title': item.title,
                'organization': item.organization,
                'description': item.description,
                'reflection': item.reflection,
                'image_url': item.image_url,
                'icon': item.icon,
            }
            for item in timeline_items
        ]
    except:
        content['decades_timeline_items'] = []
    
    # Lion Section
    try:
        lion_section = LionSection.objects.filter(is_active=True).first()
        if lion_section:
            content['lion_section'] = {
                'title': lion_section.title,
                'icon': lion_section.icon,
                'intro_text': lion_section.intro_text,
                'paragraph_1': lion_section.paragraph_1,
                'paragraph_2': lion_section.paragraph_2,
                'reflection_question': lion_section.reflection_question,
                'background_image_url': lion_section.background_image_url,
                'book_cover_image_url': lion_section.book_cover_image_url,
                'closing_quote': lion_section.closing_quote,
                **lion_section.content,
            }
    except:
        content['lion_section'] = {}
    
    return content


