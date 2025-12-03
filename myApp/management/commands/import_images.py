"""
Management command to import images from a local folder to Cloudinary
Usage: python manage.py import_images --folder path/to/images/ [--cloudinary-folder folder_name]
"""
from django.core.management.base import BaseCommand
import os
import glob

from myApp.models import MediaAsset
from myApp.utils.cloudinary_utils import upload_to_cloudinary


class Command(BaseCommand):
    help = 'Import images from a local folder to Cloudinary'

    def add_arguments(self, parser):
        parser.add_argument(
            '--folder',
            type=str,
            required=True,
            help='Path to folder containing images to import',
        )
        parser.add_argument(
            '--cloudinary-folder',
            type=str,
            default='myApp/uploads',
            help='Cloudinary folder path (default: myApp/uploads)',
        )
        parser.add_argument(
            '--extensions',
            type=str,
            default='jpg,jpeg,png,gif,webp,bmp,svg',
            help='Comma-separated list of image file extensions (default: jpg,jpeg,png,gif,webp,bmp,svg)',
        )
        parser.add_argument(
            '--recursive',
            action='store_true',
            help='Import images from subdirectories as well',
        )

    def handle(self, *args, **options):
        folder_path = options.get('folder')
        cloudinary_folder = options.get('cloudinary_folder')
        extensions = [ext.strip().lower() for ext in options.get('extensions').split(',')]
        recursive = options.get('recursive')

        # Validate folder path
        if not os.path.exists(folder_path):
            self.stdout.write(self.style.ERROR(f'Folder not found: {folder_path}'))
            return

        if not os.path.isdir(folder_path):
            self.stdout.write(self.style.ERROR(f'Path is not a directory: {folder_path}'))
            return

        # Find all image files
        image_files = []
        if recursive:
            # Search recursively
            for ext in extensions:
                pattern = os.path.join(folder_path, '**', f'*.{ext}')
                image_files.extend(glob.glob(pattern, recursive=True))
        else:
            # Search only in the specified folder
            for ext in extensions:
                pattern = os.path.join(folder_path, f'*.{ext}')
                image_files.extend(glob.glob(pattern, recursive=False))

        if not image_files:
            self.stdout.write(self.style.WARNING(f'No image files found in {folder_path}'))
            self.stdout.write(f'Supported extensions: {", ".join(extensions)}')
            return

        self.stdout.write(self.style.SUCCESS(f'Found {len(image_files)} image(s) to import'))
        self.stdout.write(f'Cloudinary folder: {cloudinary_folder}')
        self.stdout.write('')

        # Process each image
        success_count = 0
        error_count = 0

        for image_path in image_files:
            try:
                # Get filename and create title
                filename = os.path.basename(image_path)
                title = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ')
                
                # Check if image already exists (by filename)
                existing = MediaAsset.objects.filter(title=title).first()
                if existing:
                    self.stdout.write(
                        self.style.WARNING(f'⏭  Skipping {filename} (already exists)')
                    )
                    continue

                # Open and upload image
                self.stdout.write(f'📤 Uploading {filename}...', ending=' ')
                
                with open(image_path, 'rb') as f:
                    upload_result = upload_to_cloudinary(
                        f,
                        folder=cloudinary_folder,
                        public_id=None,  # Let Cloudinary generate the public_id
                    )

                # Save to database
                media_asset = MediaAsset.objects.create(
                    title=title,
                    description=f'Imported from {filename}',
                    original_url=upload_result['original_url'],
                    web_url=upload_result['web_url'],
                    thumbnail_url=upload_result['thumbnail_url'],
                    cloudinary_public_id=upload_result['public_id'],
                    folder=cloudinary_folder,
                    width=upload_result['width'],
                    height=upload_result['height'],
                    file_size=upload_result['bytes'],
                )

                self.stdout.write(self.style.SUCCESS('✓ Done'))
                success_count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))
                error_count += 1
                continue

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS(f'Import complete!'))
        self.stdout.write(f'  ✓ Successfully imported: {success_count}')
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'  ✗ Errors: {error_count}'))
        self.stdout.write(self.style.SUCCESS('=' * 50))

