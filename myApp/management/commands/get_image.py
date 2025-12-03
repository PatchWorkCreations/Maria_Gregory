"""
Management command to find and display image information by Cloudinary public ID
Usage: python manage.py get_image --public-id dkkwbqr8e
"""
from django.core.management.base import BaseCommand

from myApp.models import MediaAsset
from myApp.utils.cloudinary_utils import get_cloudinary_url


class Command(BaseCommand):
    help = 'Find image by Cloudinary public ID or search for images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--public-id',
            type=str,
            help='Cloudinary public ID to search for (e.g., dkkwbqr8e)',
        )
        parser.add_argument(
            '--search',
            type=str,
            help='Search for images by title or description',
        )
        parser.add_argument(
            '--list-all',
            action='store_true',
            help='List all images in the database',
        )
        parser.add_argument(
            '--url-only',
            action='store_true',
            help='Output only the image URL',
        )

    def handle(self, *args, **options):
        public_id = options.get('public_id')
        search_term = options.get('search')
        list_all = options.get('list_all')
        url_only = options.get('url_only')

        # Search by public ID
        if public_id:
            self.find_by_public_id(public_id, url_only)
            return

        # Search by title/description
        if search_term:
            self.search_images(search_term, url_only)
            return

        # List all images
        if list_all:
            self.list_all_images()
            return

        # Show help if no options provided
        self.stdout.write(self.style.ERROR('Please provide one of: --public-id, --search, or --list-all'))
        self.stdout.write('')
        self.stdout.write('Examples:')
        self.stdout.write('  python manage.py get_image --public-id dkkwbqr8e')
        self.stdout.write('  python manage.py get_image --search "hero"')
        self.stdout.write('  python manage.py get_image --list-all')

    def find_by_public_id(self, public_id, url_only=False):
        """Find image by Cloudinary public ID"""
        # First, try to find in database
        image = MediaAsset.objects.filter(cloudinary_public_id__icontains=public_id).first()
        
        if image:
            if url_only:
                self.stdout.write(image.original_url)
            else:
                self.stdout.write(self.style.SUCCESS('=' * 60))
                self.stdout.write(self.style.SUCCESS(f'Found image: {image.title}'))
                self.stdout.write('=' * 60)
                self.stdout.write(f'ID: {image.id}')
                self.stdout.write(f'Title: {image.title}')
                self.stdout.write(f'Public ID: {image.cloudinary_public_id}')
                self.stdout.write(f'Folder: {image.folder}')
                self.stdout.write(f'Dimensions: {image.width}x{image.height}')
                self.stdout.write(f'File Size: {image.file_size:,} bytes' if image.file_size else 'File Size: Unknown')
                self.stdout.write(f'Created: {image.created_at}')
                self.stdout.write('')
                self.stdout.write(self.style.SUCCESS('URLs:'))
                self.stdout.write(f'  Original: {image.original_url}')
                self.stdout.write(f'  Web Optimized: {image.web_url}')
                self.stdout.write(f'  Thumbnail: {image.thumbnail_url}')
                self.stdout.write('=' * 60)
            return

        # If not found in database, try to generate URL from Cloudinary
        try:
            url = get_cloudinary_url(public_id)
            if url_only:
                self.stdout.write(url)
            else:
                self.stdout.write(self.style.WARNING('Image not found in database, but Cloudinary URL exists:'))
                self.stdout.write(f'URL: {url}')
                self.stdout.write('')
                self.stdout.write('To add this image to the database, you may need to upload it through the dashboard.')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Image not found with public ID: {public_id}'))
            self.stdout.write(f'Error: {str(e)}')

    def search_images(self, search_term, url_only=False):
        """Search for images by title or description"""
        images = MediaAsset.objects.filter(
            title__icontains=search_term
        ) | MediaAsset.objects.filter(
            description__icontains=search_term
        )
        images = images.order_by('-created_at')

        if not images.exists():
            self.stdout.write(self.style.WARNING(f'No images found matching: "{search_term}"'))
            return

        count = images.count()
        self.stdout.write(self.style.SUCCESS(f'Found {count} image(s) matching "{search_term}":'))
        self.stdout.write('')

        for image in images:
            if url_only:
                self.stdout.write(image.original_url)
            else:
                self.stdout.write(f'• {image.title}')
                self.stdout.write(f'  Public ID: {image.cloudinary_public_id}')
                self.stdout.write(f'  URL: {image.original_url}')
                self.stdout.write(f'  Dimensions: {image.width}x{image.height}')
                self.stdout.write('')

    def list_all_images(self):
        """List all images in the database"""
        images = MediaAsset.objects.all().order_by('-created_at')

        if not images.exists():
            self.stdout.write(self.style.WARNING('No images found in database'))
            return

        count = images.count()
        self.stdout.write(self.style.SUCCESS(f'Total images in database: {count}'))
        self.stdout.write('')

        for image in images:
            self.stdout.write(f'• {image.title}')
            self.stdout.write(f'  ID: {image.id} | Public ID: {image.cloudinary_public_id}')
            self.stdout.write(f'  URL: {image.original_url}')
            self.stdout.write(f'  Size: {image.width}x{image.height} | Created: {image.created_at.strftime("%Y-%m-%d")}')
            self.stdout.write('')

