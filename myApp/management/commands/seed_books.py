"""
Management command to seed the database with books section content
Run with: python manage.py seed_books
"""
from django.core.management.base import BaseCommand
from myApp.models import BooksSection, PublishedBook


class Command(BaseCommand):
    help = 'Seeds the database with books section content'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed books content...'))

        # 1. Books Section
        books_section, created = BooksSection.objects.get_or_create(pk=1)
        books_section.title = "Books by Maria Gregory"
        books_section.subtitle = "Stories, reflections, and faith-rooted writings"
        books_section.description = (
            "These books were written for people who carry a lot—leaders, caregivers, "
            "builders, and believers—who rarely pause to tend to their own souls. "
            "Each one invites you to slow down, listen deeply, and rediscover strength, "
            "hope, and courage in quieter ways."
        )
        books_section.show_publishing_service = True
        books_section.publishing_service_title = "Thinking of Publishing Your Own Book?"
        books_section.publishing_service_description = (
            "I’ve walked the full publishing journey—from fragile first drafts to finished books "
            "held in trembling hands. If you’re carrying a story, a message, or a legacy that needs "
            "to be shared, I’d be honored to help you bring it to life with care and clarity."
        )
        books_section.publishing_service_button_text = "Let’s Talk About Your Book"
        books_section.publishing_service_button_url = "#contact"
        books_section.is_active = True
        books_section.save()

        self.stdout.write(self.style.SUCCESS('✓ Books section created'))

        # 2. Published Books
        PublishedBook.objects.all().delete()

        books = [
            {
                'title': 'Conversations Through Psalms',
                'subtitle': 'When Prayer Feels Hard, Let the Psalms Speak',
                'description': (
                    "Written as gentle conversations rather than formal prayers, this book walks "
                    "with readers through the Psalms during seasons of illness, grief, confusion, "
                    "and quiet waiting. Originally created for a dear friend recovering from a stroke, "
                    "it became a companion for anyone who doesn't know what to say—but still wants to pray."
                ),
                'cover_image_url': 'https://m.media-amazon.com/images/I/51kWvC0W8rL._SX342_SY445_FMwebp_.jpg',
                'publisher': 'Independent',
                'publication_year': '2024',
                'purchase_url': 'https://www.amazon.com/-/he/Maria-Gregory/dp/B0DR4L7PW7',
                'amazon_url': 'https://www.amazon.com/-/he/Maria-Gregory/dp/B0DR4L7PW7',
                'sort_order': 1
            },
            {
                'title': "The Lion You Don't See",
                'subtitle': 'Strength, Faith, and the Courage to Keep Going',
                'description': (
                    "This is a book for the strong ones—the ones who keep showing up, holding others together, "
                    "and pressing forward even when unseen. Through story and reflection, it reminds readers "
                    "that courage isn't always loud, and faith often grows strongest in hidden places."
                ),
                'cover_image_url': 'https://m.media-amazon.com/images/I/81awF3C+pdL._SY466_.jpg',
                'publisher': 'Independent',
                'publication_year': '2023',
                'purchase_url': 'https://www.amazon.com/Lion-You-Dont-See-Editions-ebook/dp/B0DL5BFWTS',
                'amazon_url': 'https://www.amazon.com/Lion-You-Dont-See-Editions-ebook/dp/B0DL5BFWTS',
                'sort_order': 2
            },
            {
                'title': 'The Christmas Lion Who Shows the Way',
                'subtitle': 'A Story of Light, Courage, and Hope',
                'description': (
                    "A tender Christmas story for children and adults alike, this book gently reminds us "
                    "that even in the darkest nights, love and light still lead. Perfect for families, "
                    "quiet evenings, and anyone who needs a reminder that hope always finds a way home."
                ),
                'cover_image_url': 'https://m.media-amazon.com/images/I/71ZwWGj-Z-L._SY466_.jpg',
                'publisher': 'Independent',
                'publication_year': '2023',
                'purchase_url': 'https://www.amazon.com/Christmas-Lion-Who-Shows-Way/dp/B0DPQ9VP34',
                'amazon_url': 'https://www.amazon.com/Christmas-Lion-Who-Shows-Way/dp/B0DPQ9VP34',
                'sort_order': 3
            },
        ]

        for book_data in books:
            book = PublishedBook.objects.create(
                books_section=books_section,
                **book_data
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Created book: {book.title}'))

        # 3. Publishing Service Features
        publishing_features = [
            {
                'title': 'Story Discernment',
                'description': 'Helping you clarify what your story is truly about—and why it matters'
            },
            {
                'title': 'Manuscript Shaping',
                'description': 'Gentle guidance to strengthen flow, voice, and emotional clarity'
            },
            {
                'title': 'Publishing Pathways',
                'description': 'Support navigating self-publishing, hybrid, or assisted publishing'
            },
            {
                'title': 'Legacy & Launch Support',
                'description': 'Thoughtful planning for releasing your book into the world with purpose'
            }
        ]

        books_section.content = {
            'publishing_service_features': publishing_features
        }
        books_section.save()

        self.stdout.write(self.style.SUCCESS('✓ Publishing service features added'))
        self.stdout.write(self.style.SUCCESS('\n✅ Books content seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('Manage books at /dashboard/'))
