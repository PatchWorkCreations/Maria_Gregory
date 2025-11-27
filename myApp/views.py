from django.shortcuts import render
from .content_helpers import get_homepage_content_from_db

def home(request):
    """Homepage view - uses database if available, falls back to empty content"""
    try:
        # Try to get content from database
        content = get_homepage_content_from_db()
    except Exception as e:
        # Fall back to empty content if database is not set up
        content = {}
    
    context = {
        "content": content
    }
    return render(request, "myApp/home.html", context)
