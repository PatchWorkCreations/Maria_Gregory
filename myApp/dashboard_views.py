"""
Dashboard views for content management
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
import json
import os

from .models import (
    MediaAsset, SEO, Navigation, Hero, About, Stat, Service, ServicesSection,
    Portfolio, PortfolioProject, Testimonial, FAQ, FAQSection, Contact,
    ContactInfo, ContactFormField, SocialLink, Footer, DecadesSection, DecadesTimelineItem,
    LionSection
)
from .utils.cloudinary_utils import upload_to_cloudinary


# Authentication Views
def dashboard_login(request):
    """Login view for dashboard"""
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('dashboard:index')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'dashboard/login.html')


@login_required
def dashboard_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('dashboard:login')


# Dashboard Home
@login_required
def dashboard_home(request):
    """Main dashboard page"""
    context = {
        'total_images': MediaAsset.objects.count(),
        'total_nav_items': Navigation.objects.count(),
        'total_services': Service.objects.count(),
        'total_testimonials': Testimonial.objects.count(),
        'total_contact_info': ContactInfo.objects.count(),
        'total_contact_form_fields': ContactFormField.objects.count(),
        'recent_images': MediaAsset.objects.all()[:5],
    }
    return render(request, 'dashboard/index.html', context)


# Image Upload and Gallery
@login_required
@csrf_exempt
def upload_image(request):
    """Upload image(s) to Cloudinary - supports single or multiple files"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        # Check Cloudinary configuration
        import cloudinary
        import os
        from pathlib import Path
        from dotenv import load_dotenv
        
        # Reload .env file to ensure we have the latest credentials
        # BASE_DIR should be project root (2 levels up from myApp/dashboard_views.py)
        BASE_DIR = Path(__file__).resolve().parent.parent
        load_dotenv(BASE_DIR / '.env', override=True)
        
        cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME', '')
        api_key = os.getenv('CLOUDINARY_API_KEY', '')
        api_secret = os.getenv('CLOUDINARY_API_SECRET', '')
        
        if not cloud_name or not api_key or not api_secret:
            env_file_path = BASE_DIR / '.env'
            env_exists = env_file_path.exists()
            return JsonResponse({
                'error': f'Cloudinary not configured. Please set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET in your .env file. (.env file exists: {env_exists})'
            }, status=500)
        
        # Check if we have 'image' (single) or 'images[]' (multiple)
        # Try multiple files first, then single file for backward compatibility
        image_files = request.FILES.getlist('images[]') or request.FILES.getlist('image')
        
        # Also check for single file upload (backward compatibility)
        if not image_files and 'image' in request.FILES:
            image_files = [request.FILES['image']]
        
        if not image_files:
            return JsonResponse({'error': 'No image file(s) provided'}, status=400)
        
        folder = request.POST.get('folder', 'myApp/uploads')
        default_title = request.POST.get('title', '')
        default_description = request.POST.get('description', '')
        
        uploaded_images = []
        errors = []
        
        # Process each image
        for idx, image_file in enumerate(image_files):
            try:
                # Use provided title/description for first image, or filename for others
                title = default_title if idx == 0 and default_title else image_file.name.rsplit('.', 1)[0]
                description = default_description if idx == 0 else ''
                
                # Upload to Cloudinary
                upload_result = upload_to_cloudinary(image_file, folder=folder)
                
                # Check if image already exists (prevent duplicates)
                public_id = upload_result['public_id']
                existing_asset = MediaAsset.objects.filter(cloudinary_public_id=public_id).first()
                
                if existing_asset:
                    # Image already exists, skip creating duplicate
                    uploaded_images.append({
                        'id': existing_asset.id,
                        'title': existing_asset.title,
                        'original_url': existing_asset.original_url,
                        'web_url': existing_asset.web_url,
                        'thumbnail_url': existing_asset.thumbnail_url,
                    })
                    continue
                
                # Save to database
                media_asset = MediaAsset.objects.create(
                    title=title,
                    description=description,
                    original_url=upload_result['original_url'],
                    web_url=upload_result['web_url'],
                    thumbnail_url=upload_result['thumbnail_url'],
                    cloudinary_public_id=public_id,
                    folder=folder,
                    width=upload_result['width'],
                    height=upload_result['height'],
                    file_size=upload_result['bytes'],
                )
                
                uploaded_images.append({
                    'id': media_asset.id,
                    'title': media_asset.title,
                    'original_url': media_asset.original_url,
                    'web_url': media_asset.web_url,
                    'thumbnail_url': media_asset.thumbnail_url,
                })
            except Exception as e:
                import traceback
                error_msg = str(e)
                # Log full traceback for debugging
                print(f"Error uploading {image_file.name}: {error_msg}")
                print(traceback.format_exc())
                errors.append({
                    'filename': image_file.name,
                    'error': error_msg
                })
        
        # Return results
        if uploaded_images:
            return JsonResponse({
                'success': True,
                'images': uploaded_images,
                'count': len(uploaded_images),
                'errors': errors if errors else None
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'All uploads failed. Check server console for details.',
                'errors': errors
            }, status=400)
    
    except Exception as e:
        import traceback
        error_msg = str(e)
        print(f"Upload error: {error_msg}")
        print(traceback.format_exc())
        return JsonResponse({'error': error_msg}, status=500)


@login_required
def gallery(request):
    """Image gallery view"""
    images = MediaAsset.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(images, 24)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Support JSON response for image picker
    if request.GET.get('format') == 'json' or request.GET.get('json'):
        images_data = []
        for img in page_obj:
            images_data.append({
                'id': img.id,
                'title': img.title,
                'original_url': img.original_url,
                'web_url': img.web_url,
                'thumbnail_url': img.thumbnail_url,
            })
        
        return JsonResponse({
            'images': images_data,
            'pagination': {
                'number': page_obj.number,
                'num_pages': paginator.num_pages,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            }
        })
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'dashboard/gallery.html', context)


# SEO Views
@login_required
def seo_edit(request):
    """Edit SEO settings"""
    seo, created = SEO.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        seo.page_title = request.POST.get('page_title', '')
        seo.meta_description = request.POST.get('meta_description', '')
        seo.meta_keywords = request.POST.get('meta_keywords', '')
        seo.og_title = request.POST.get('og_title', '')
        seo.og_description = request.POST.get('og_description', '')
        seo.og_image = request.POST.get('og_image', '')
        seo.twitter_card = request.POST.get('twitter_card', 'summary_large_image')
        seo.canonical_url = request.POST.get('canonical_url', '')
        seo.save()
        messages.success(request, 'SEO settings updated successfully!')
        return redirect('dashboard:seo_edit')
    
    context = {'seo': seo}
    return render(request, 'dashboard/seo_edit.html', context)


# Navigation Views
@login_required
def navigation_edit(request):
    """Edit navigation items"""
    nav_items = Navigation.objects.all()
    
    if request.method == 'POST':
        # Handle delete
        if 'delete_id' in request.POST:
            nav_id = request.POST.get('delete_id')
            nav = get_object_or_404(Navigation, id=nav_id)
            nav.delete()
            messages.success(request, 'Navigation item deleted!')
            return redirect('dashboard:navigation_edit')
        
        # Handle add/edit
        nav_id = request.POST.get('id')
        if nav_id:
            nav = get_object_or_404(Navigation, id=nav_id)
        else:
            nav = Navigation()
        
        nav.label = request.POST.get('label', '')
        nav.url = request.POST.get('url', '')
        nav.order = int(request.POST.get('order', 0))
        nav.is_external = request.POST.get('is_external') == 'on'
        nav.is_active = request.POST.get('is_active') == 'on'
        nav.save()
        
        messages.success(request, 'Navigation item saved!')
        return redirect('dashboard:navigation_edit')
    
    context = {'nav_items': nav_items}
    return render(request, 'dashboard/navigation_edit.html', context)


# Hero Views
@login_required
def hero_edit(request):
    """Edit hero section"""
    hero, created = Hero.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        hero.title = request.POST.get('title', '')
        hero.subtitle = request.POST.get('subtitle', '')
        hero.description = request.POST.get('description', '')
        hero.button_text = request.POST.get('button_text', '')
        hero.button_url = request.POST.get('button_url', '')
        hero.background_image_url = request.POST.get('background_image_url', '')
        hero.is_active = request.POST.get('is_active') == 'on'
        
        # Handle JSON content
        content_json = request.POST.get('content', '{}')
        try:
            hero.content = json.loads(content_json)
        except:
            hero.content = {}
        
        hero.save()
        messages.success(request, 'Hero section updated!')
        return redirect('dashboard:hero_edit')
    
    context = {'hero': hero}
    return render(request, 'dashboard/hero_edit.html', context)


# About Views
@login_required
def about_edit(request):
    """Edit about section"""
    about, created = About.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        about.title = request.POST.get('title', '')
        about.subtitle = request.POST.get('subtitle', '')
        about.description = request.POST.get('description', '')
        about.image_url = request.POST.get('image_url', '')
        about.quote = request.POST.get('quote', '')
        about.is_active = request.POST.get('is_active') == 'on'
        
        content_json = request.POST.get('content', '{}')
        try:
            about.content = json.loads(content_json)
        except:
            about.content = {}
        
        about.save()
        messages.success(request, 'About section updated!')
        return redirect('dashboard:about_edit')
    
    context = {'about': about}
    return render(request, 'dashboard/about_edit.html', context)


# Stats Views
@login_required
def stats_list(request):
    """List all statistics"""
    stats = Stat.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            stat_id = request.POST.get('delete_id')
            stat = get_object_or_404(Stat, id=stat_id)
            stat.delete()
            messages.success(request, 'Statistic deleted!')
            return redirect('dashboard:stats_list')
    
    context = {'stats': stats}
    return render(request, 'dashboard/stats_list.html', context)


@login_required
def stat_edit(request, stat_id=None):
    """Edit or create a statistic"""
    if stat_id:
        stat = get_object_or_404(Stat, id=stat_id)
    else:
        stat = Stat()
    
    if request.method == 'POST':
        stat.label = request.POST.get('label', '')
        stat.value = request.POST.get('value', '')
        stat.description = request.POST.get('description', '')
        stat.icon = request.POST.get('icon', '')
        stat.sort_order = int(request.POST.get('sort_order', 0))
        stat.is_active = request.POST.get('is_active') == 'on'
        stat.save()
        messages.success(request, 'Statistic saved!')
        return redirect('dashboard:stats_list')
    
    context = {'stat': stat}
    return render(request, 'dashboard/stat_edit.html', context)


# Services Views
@login_required
def services_list(request):
    """List all services"""
    services = Service.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            service_id = request.POST.get('delete_id')
            service = get_object_or_404(Service, id=service_id)
            service.delete()
            messages.success(request, 'Service deleted!')
            return redirect('dashboard:services_list')
    
    context = {'services': services}
    return render(request, 'dashboard/services_list.html', context)


@login_required
def service_edit(request, service_id=None):
    """Edit or create a service"""
    if service_id:
        service = get_object_or_404(Service, id=service_id)
    else:
        service = Service()
    
    if request.method == 'POST':
        service.title = request.POST.get('title', '')
        service.description = request.POST.get('description', '')
        service.icon = request.POST.get('icon', '')
        service.image_url = request.POST.get('image_url', '')
        service.sort_order = int(request.POST.get('sort_order', 0))
        service.is_active = request.POST.get('is_active') == 'on'
        
        content_json = request.POST.get('content', '{}')
        try:
            service.content = json.loads(content_json)
        except:
            service.content = {}
        
        service.save()
        messages.success(request, 'Service saved!')
        return redirect('dashboard:services_list')
    
    context = {'service': service}
    return render(request, 'dashboard/service_edit.html', context)


@login_required
def services_section_edit(request):
    """Edit services section"""
    section, created = ServicesSection.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        section.title = request.POST.get('title', '')
        section.subtitle = request.POST.get('subtitle', '')
        section.description = request.POST.get('description', '')
        section.is_active = request.POST.get('is_active') == 'on'
        
        content_json = request.POST.get('content', '{}')
        try:
            section.content = json.loads(content_json)
        except:
            section.content = {}
        
        section.save()
        messages.success(request, 'Services section updated!')
        return redirect('dashboard:services_section_edit')
    
    context = {'section': section}
    return render(request, 'dashboard/services_section_edit.html', context)


# Portfolio Views
@login_required
def portfolio_edit(request):
    """Edit portfolio section"""
    portfolio, created = Portfolio.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        portfolio.title = request.POST.get('title', '')
        portfolio.subtitle = request.POST.get('subtitle', '')
        portfolio.description = request.POST.get('description', '')
        portfolio.is_active = request.POST.get('is_active') == 'on'
        
        content_json = request.POST.get('content', '{}')
        try:
            portfolio.content = json.loads(content_json)
        except:
            portfolio.content = {}
        
        portfolio.save()
        messages.success(request, 'Portfolio section updated!')
        return redirect('dashboard:portfolio_edit')
    
    context = {'portfolio': portfolio}
    return render(request, 'dashboard/portfolio_edit.html', context)


@login_required
def portfolio_projects_list(request):
    """List all portfolio projects"""
    projects = PortfolioProject.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            project_id = request.POST.get('delete_id')
            project = get_object_or_404(PortfolioProject, id=project_id)
            project.delete()
            messages.success(request, 'Project deleted!')
            return redirect('dashboard:portfolio_projects_list')
    
    context = {'projects': projects}
    return render(request, 'dashboard/portfolio_projects_list.html', context)


@login_required
def portfolio_project_edit(request, project_id=None):
    """Edit or create a portfolio project"""
    if project_id:
        project = get_object_or_404(PortfolioProject, id=project_id)
    else:
        project = PortfolioProject()
    
    if request.method == 'POST':
        project.title = request.POST.get('title', '')
        project.description = request.POST.get('description', '')
        project.image_url = request.POST.get('image_url', '')
        project.project_url = request.POST.get('project_url', '')
        project.category = request.POST.get('category', '')
        project.sort_order = int(request.POST.get('sort_order', 0))
        project.is_active = request.POST.get('is_active') == 'on'
        
        content_json = request.POST.get('content', '{}')
        try:
            project.content = json.loads(content_json)
        except:
            project.content = {}
        
        project.save()
        messages.success(request, 'Project saved!')
        return redirect('dashboard:portfolio_projects_list')
    
    context = {'project': project}
    return render(request, 'dashboard/portfolio_project_edit.html', context)


# Testimonials Views
@login_required
def testimonials_list(request):
    """List all testimonials"""
    testimonials = Testimonial.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            testimonial_id = request.POST.get('delete_id')
            testimonial = get_object_or_404(Testimonial, id=testimonial_id)
            testimonial.delete()
            messages.success(request, 'Testimonial deleted!')
            return redirect('dashboard:testimonials_list')
    
    context = {'testimonials': testimonials}
    return render(request, 'dashboard/testimonials_list.html', context)


@login_required
def testimonial_edit(request, testimonial_id=None):
    """Edit or create a testimonial"""
    if testimonial_id:
        testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    else:
        testimonial = Testimonial()
    
    if request.method == 'POST':
        testimonial.name = request.POST.get('name', '')
        testimonial.role = request.POST.get('role', '')
        testimonial.company = request.POST.get('company', '')
        testimonial.content = request.POST.get('content', '')
        testimonial.image_url = request.POST.get('image_url', '')
        testimonial.rating = int(request.POST.get('rating', 5)) if request.POST.get('rating') else None
        testimonial.sort_order = int(request.POST.get('sort_order', 0))
        testimonial.is_active = request.POST.get('is_active') == 'on'
        testimonial.save()
        messages.success(request, 'Testimonial saved!')
        return redirect('dashboard:testimonials_list')
    
    context = {'testimonial': testimonial}
    return render(request, 'dashboard/testimonial_edit.html', context)


# FAQ Views
@login_required
def faqs_list(request):
    """List all FAQs"""
    faqs = FAQ.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            faq_id = request.POST.get('delete_id')
            faq = get_object_or_404(FAQ, id=faq_id)
            faq.delete()
            messages.success(request, 'FAQ deleted!')
            return redirect('dashboard:faqs_list')
    
    context = {'faqs': faqs}
    return render(request, 'dashboard/faqs_list.html', context)


@login_required
def faq_edit(request, faq_id=None):
    """Edit or create a FAQ"""
    if faq_id:
        faq = get_object_or_404(FAQ, id=faq_id)
    else:
        faq = FAQ()
    
    if request.method == 'POST':
        faq.question = request.POST.get('question', '')
        faq.answer = request.POST.get('answer', '')
        faq.category = request.POST.get('category', '')
        faq.sort_order = int(request.POST.get('sort_order', 0))
        faq.is_active = request.POST.get('is_active') == 'on'
        faq.save()
        messages.success(request, 'FAQ saved!')
        return redirect('dashboard:faqs_list')
    
    context = {'faq': faq}
    return render(request, 'dashboard/faq_edit.html', context)


@login_required
def faq_section_edit(request):
    """Edit FAQ section"""
    section, created = FAQSection.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        section.title = request.POST.get('title', '')
        section.subtitle = request.POST.get('subtitle', '')
        section.description = request.POST.get('description', '')
        section.is_active = request.POST.get('is_active') == 'on'
        
        content_json = request.POST.get('content', '{}')
        try:
            section.content = json.loads(content_json)
        except:
            section.content = {}
        
        section.save()
        messages.success(request, 'FAQ section updated!')
        return redirect('dashboard:faq_section_edit')
    
    context = {'section': section}
    return render(request, 'dashboard/faq_section_edit.html', context)


# Call To Action Views
@login_required
def cta_edit(request):
    """Edit Call To Action section (upper dark section)"""
    contact, created = Contact.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        contact.cta_title = request.POST.get('cta_title', '')
        contact.cta_subtitle = request.POST.get('cta_subtitle', '')
        contact.cta_description = request.POST.get('cta_description', '')
        contact.cta_quote = request.POST.get('cta_quote', '')
        # Buttons
        contact.cta_button1_text = request.POST.get('cta_button1_text', '')
        contact.cta_button1_url = request.POST.get('cta_button1_url', '')
        contact.cta_button2_text = request.POST.get('cta_button2_text', '')
        contact.cta_button2_url = request.POST.get('cta_button2_url', '')
        contact.cta_button3_text = request.POST.get('cta_button3_text', '')
        contact.cta_button3_url = request.POST.get('cta_button3_url', '')
        contact.is_active = request.POST.get('is_active') == 'on'
        
        contact.save()
        messages.success(request, 'Call To Action section updated!')
        return redirect('dashboard:cta_edit')
    
    context = {'contact': contact}
    return render(request, 'dashboard/cta_edit.html', context)


# Contact Views
@login_required
def contact_edit(request):
    """Edit contact section (lower white section)"""
    contact, created = Contact.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        # Contact Section (Lower White Section)
        contact.title = request.POST.get('title', '')
        contact.subtitle = request.POST.get('subtitle', '')
        contact.description = request.POST.get('description', '')
        contact.is_active = request.POST.get('is_active') == 'on'
        
        content_json = request.POST.get('content', '{}')
        try:
            contact.content = json.loads(content_json)
        except:
            contact.content = {}
        
        contact.save()
        messages.success(request, 'Contact section updated!')
        return redirect('dashboard:contact_edit')
    
    context = {'contact': contact}
    return render(request, 'dashboard/contact_edit.html', context)


@login_required
def contact_info_list(request):
    """List all contact info items"""
    contact_infos = ContactInfo.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            info_id = request.POST.get('delete_id')
            info = get_object_or_404(ContactInfo, id=info_id)
            info.delete()
            messages.success(request, 'Contact info deleted!')
            return redirect('dashboard:contact_info_list')
    
    context = {'contact_infos': contact_infos}
    return render(request, 'dashboard/contact_info_list.html', context)


@login_required
def contact_info_edit(request, info_id=None):
    """Edit or create contact info"""
    if info_id:
        info = get_object_or_404(ContactInfo, id=info_id)
    else:
        info = ContactInfo()
    
    if request.method == 'POST':
        info.type = request.POST.get('type', 'other')
        info.label = request.POST.get('label', '')
        info.value = request.POST.get('value', '')
        info.icon = request.POST.get('icon', '')
        info.sort_order = int(request.POST.get('sort_order', 0))
        info.is_active = request.POST.get('is_active') == 'on'
        info.save()
        messages.success(request, 'Contact info saved!')
        return redirect('dashboard:contact_info_list')
    
    context = {'info': info}
    return render(request, 'dashboard/contact_info_edit.html', context)


@login_required
def contact_form_fields_list(request):
    """List all contact form fields"""
    fields = ContactFormField.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            field_id = request.POST.get('delete_id')
            field = get_object_or_404(ContactFormField, id=field_id)
            field.delete()
            messages.success(request, 'Form field deleted!')
            return redirect('dashboard:contact_form_fields_list')
    
    context = {'fields': fields}
    return render(request, 'dashboard/contact_form_fields_list.html', context)


@login_required
def contact_form_field_edit(request, field_id=None):
    """Edit or create contact form field"""
    if field_id:
        field = get_object_or_404(ContactFormField, id=field_id)
    else:
        field = ContactFormField()
    
    if request.method == 'POST':
        field.label = request.POST.get('label', '')
        field.field_type = request.POST.get('field_type', 'text')
        field.placeholder = request.POST.get('placeholder', '')
        field.is_required = request.POST.get('is_required') == 'on'
        field.sort_order = int(request.POST.get('sort_order', 0))
        field.is_active = request.POST.get('is_active') == 'on'
        
        # Handle options - can come as JSON string or as textarea (one per line)
        options_json = request.POST.get('options', '[]')
        options_text = request.POST.get('options_text', '')
        
        if options_text:
            # Convert textarea (one per line) to list
            options_list = [opt.strip() for opt in options_text.split('\n') if opt.strip()]
            field.options = options_list
        else:
            try:
                field.options = json.loads(options_json)
            except:
                field.options = []
        
        field.save()
        messages.success(request, 'Form field saved!')
        return redirect('dashboard:contact_form_fields_list')
    
    context = {'field': field}
    return render(request, 'dashboard/contact_form_field_edit.html', context)


# Social Links Views
@login_required
def social_links_list(request):
    """List all social links"""
    social_links = SocialLink.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            link_id = request.POST.get('delete_id')
            link = get_object_or_404(SocialLink, id=link_id)
            link.delete()
            messages.success(request, 'Social link deleted!')
            return redirect('dashboard:social_links_list')
    
    context = {'social_links': social_links}
    return render(request, 'dashboard/social_links_list.html', context)


@login_required
def social_link_edit(request, link_id=None):
    """Edit or create social link"""
    if link_id:
        link = get_object_or_404(SocialLink, id=link_id)
    else:
        link = SocialLink()
    
    if request.method == 'POST':
        link.platform = request.POST.get('platform', 'other')
        link.label = request.POST.get('label', '')
        link.url = request.POST.get('url', '')
        link.icon = request.POST.get('icon', '')
        link.sort_order = int(request.POST.get('sort_order', 0))
        link.is_active = request.POST.get('is_active') == 'on'
        link.save()
        messages.success(request, 'Social link saved!')
        return redirect('dashboard:social_links_list')
    
    context = {'link': link}
    return render(request, 'dashboard/social_link_edit.html', context)


# Footer Views
@login_required
def footer_edit(request):
    """Edit footer"""
    footer, created = Footer.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        footer.copyright_text = request.POST.get('copyright_text', '')
        footer.is_active = request.POST.get('is_active') == 'on'
        
        content_json = request.POST.get('content', '{}')
        try:
            footer.content = json.loads(content_json)
        except:
            footer.content = {}
        
        footer.save()
        messages.success(request, 'Footer updated!')
        return redirect('dashboard:footer_edit')
    
    context = {'footer': footer}
    return render(request, 'dashboard/footer_edit.html', context)


# Decades Section Views
@login_required
def decades_section_edit(request):
    """Edit Decades of Walking With Leaders section"""
    section, created = DecadesSection.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        section.title = request.POST.get('title', '')
        section.subtitle = request.POST.get('subtitle', '')
        section.description = request.POST.get('description', '')
        section.closing_quote = request.POST.get('closing_quote', '')
        section.is_active = request.POST.get('is_active') == 'on'
        
        content_json = request.POST.get('content', '{}')
        try:
            section.content = json.loads(content_json)
        except:
            section.content = {}
        
        section.save()
        messages.success(request, 'Decades section updated!')
        return redirect('dashboard:decades_section_edit')
    
    context = {'section': section}
    return render(request, 'dashboard/decades_section_edit.html', context)


@login_required
def decades_timeline_items_list(request):
    """List all decades timeline items"""
    items = DecadesTimelineItem.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            item_id = request.POST.get('delete_id')
            item = get_object_or_404(DecadesTimelineItem, id=item_id)
            item.delete()
            messages.success(request, 'Timeline item deleted!')
            return redirect('dashboard:decades_timeline_items_list')
    
    context = {'items': items}
    return render(request, 'dashboard/decades_timeline_items_list.html', context)


@login_required
def decades_timeline_item_edit(request, item_id=None):
    """Edit or create a decades timeline item"""
    if item_id:
        item = get_object_or_404(DecadesTimelineItem, id=item_id)
    else:
        item = DecadesTimelineItem()
    
    if request.method == 'POST':
        item.period = request.POST.get('period', '')
        item.title = request.POST.get('title', '')
        item.organization = request.POST.get('organization', '')
        item.description = request.POST.get('description', '')
        item.reflection = request.POST.get('reflection', '')
        item.image_url = request.POST.get('image_url', '')
        item.icon = request.POST.get('icon', '')
        item.sort_order = int(request.POST.get('sort_order', 0))
        item.is_active = request.POST.get('is_active') == 'on'
        
        # Link to section if it exists
        section, _ = DecadesSection.objects.get_or_create(pk=1)
        item.section = section
        
        item.save()
        messages.success(request, 'Timeline item saved!')
        return redirect('dashboard:decades_timeline_items_list')
    
    context = {'item': item}
    return render(request, 'dashboard/decades_timeline_item_edit.html', context)


# Lion Section Views
@login_required
def lion_section_edit(request):
    """Edit The Lion You Don't See section"""
    section, created = LionSection.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        section.title = request.POST.get('title', '')
        section.icon = request.POST.get('icon', 'fas fa-star')
        section.intro_text = request.POST.get('intro_text', '')
        section.paragraph_1 = request.POST.get('paragraph_1', '')
        section.paragraph_2 = request.POST.get('paragraph_2', '')
        section.reflection_question = request.POST.get('reflection_question', '')
        section.background_image_url = request.POST.get('background_image_url', '')
        section.book_cover_image_url = request.POST.get('book_cover_image_url', '')
        section.closing_quote = request.POST.get('closing_quote', '')
        section.is_active = request.POST.get('is_active') == 'on'
        
        content_json = request.POST.get('content', '{}')
        try:
            section.content = json.loads(content_json)
        except:
            section.content = {}
        
        section.save()
        messages.success(request, 'Lion section updated!')
        return redirect('dashboard:lion_section_edit')
    
    context = {'section': section}
    return render(request, 'dashboard/lion_section_edit.html', context)


