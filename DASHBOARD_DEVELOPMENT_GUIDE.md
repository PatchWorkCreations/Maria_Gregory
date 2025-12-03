# Dashboard Development Guide

## How to Add a New Function to the Website Dashboard

This guide explains the step-by-step process for adding a new feature/function to the Maria Gregory website dashboard. The dashboard follows a consistent pattern that makes adding new features straightforward.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture Overview](#architecture-overview)
3. [Step-by-Step Guide](#step-by-step-guide)
4. [Example: Adding a "Blog Posts" Feature](#example-adding-a-blog-posts-feature)
5. [Common Patterns](#common-patterns)
6. [Best Practices](#best-practices)

---

## Overview

The dashboard is built using Django and follows the Model-View-Template (MVT) pattern. Each feature typically consists of:

- **Model**: Database structure (`models.py`)
- **View**: Business logic (`dashboard_views.py`)
- **URL**: Route configuration (`dashboard_urls.py`)
- **Template**: HTML interface (`templates/dashboard/`)

---

## Architecture Overview

### File Structure

```
myProject/
├── myApp/
│   ├── models.py              # Database models
│   ├── dashboard_views.py      # View functions
│   ├── dashboard_urls.py       # URL routing
│   └── templates/
│       └── dashboard/
│           ├── base.html       # Base template with sidebar
│           └── [feature].html  # Feature-specific templates
└── myProject/
    └── urls.py                 # Main URL configuration
```

### Key Components

1. **Models** (`models.py`): Define database structure
2. **Views** (`dashboard_views.py`): Handle HTTP requests and responses
3. **URLs** (`dashboard_urls.py`): Map URLs to views
4. **Templates** (`templates/dashboard/`): HTML user interface

---

## Step-by-Step Guide

### Step 1: Define the Model

Add your model to `myApp/models.py`. Models define the database structure.

**Pattern for Single Instance (like SEO, Hero):**
```python
class YourFeature(models.Model):
    """Description of your feature"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = JSONField(default=dict, blank=True)  # For flexible data
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Your Features"

    def __str__(self):
        return self.title
```

**Pattern for Multiple Items (like Services, Testimonials):**
```python
class YourItem(models.Model):
    """Description of individual items"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.title
```

**After adding the model:**
1. Create migration: `python manage.py makemigrations`
2. Apply migration: `python manage.py migrate`

---

### Step 2: Create View Functions

Add view functions to `myApp/dashboard_views.py`. Import your model at the top:

```python
from .models import YourFeature, YourItem
```

#### For Single Instance Features (Edit Only)

```python
@login_required
def your_feature_edit(request):
    """Edit your feature"""
    feature, created = YourFeature.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        feature.title = request.POST.get('title', '')
        feature.description = request.POST.get('description', '')
        feature.is_active = request.POST.get('is_active') == 'on'
        
        # Handle JSON content if needed
        content_json = request.POST.get('content', '{}')
        try:
            feature.content = json.loads(content_json)
        except:
            feature.content = {}
        
        feature.save()
        messages.success(request, 'Feature updated!')
        return redirect('dashboard:your_feature_edit')
    
    context = {'feature': feature}
    return render(request, 'dashboard/your_feature_edit.html', context)
```

#### For Multiple Items (List + Edit)

**List View:**
```python
@login_required
def your_items_list(request):
    """List all items"""
    items = YourItem.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            item_id = request.POST.get('delete_id')
            item = get_object_or_404(YourItem, id=item_id)
            item.delete()
            messages.success(request, 'Item deleted!')
            return redirect('dashboard:your_items_list')
    
    context = {'items': items}
    return render(request, 'dashboard/your_items_list.html', context)
```

**Edit/Create View:**
```python
@login_required
def your_item_edit(request, item_id=None):
    """Edit or create an item"""
    if item_id:
        item = get_object_or_404(YourItem, id=item_id)
    else:
        item = YourItem()
    
    if request.method == 'POST':
        item.title = request.POST.get('title', '')
        item.description = request.POST.get('description', '')
        item.sort_order = int(request.POST.get('sort_order', 0))
        item.is_active = request.POST.get('is_active') == 'on'
        item.save()
        messages.success(request, 'Item saved!')
        return redirect('dashboard:your_items_list')
    
    context = {'item': item}
    return render(request, 'dashboard/your_item_edit.html', context)
```

---

### Step 3: Add URL Routes

Add routes to `myApp/dashboard_urls.py`:

**For Single Instance:**
```python
path('your-feature/', dashboard_views.your_feature_edit, name='your_feature_edit'),
```

**For Multiple Items:**
```python
path('your-items/', dashboard_views.your_items_list, name='your_items_list'),
path('your-items/new/', dashboard_views.your_item_edit, name='your_item_new'),
path('your-items/<int:item_id>/', dashboard_views.your_item_edit, name='your_item_edit'),
```

**Important:** Place routes in a logical order. The more specific routes (with IDs) should come after the general ones.

---

### Step 4: Create Templates

Create HTML templates in `myApp/templates/dashboard/`.

#### Template for Single Instance (Edit Form)

Create `your_feature_edit.html`:

```html
{% extends "dashboard/base.html" %}

{% block title %}Edit Your Feature{% endblock %}

{% block content %}
<div class="mb-8">
    <h1 class="text-3xl font-bold text-navy-900 mb-2">Edit Your Feature</h1>
    <p class="text-gray-600">Manage your feature settings</p>
</div>

<form method="post" class="bg-white rounded-lg shadow p-6">
    {% csrf_token %}
    
    <div class="mb-6">
        <label class="block text-gray-700 font-medium mb-2">Title</label>
        <input type="text" name="title" value="{{ feature.title|default:'' }}" 
               class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-navy-500" required>
    </div>
    
    <div class="mb-6">
        <label class="block text-gray-700 font-medium mb-2">Description</label>
        <textarea name="description" rows="5" 
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-navy-500">{{ feature.description|default:'' }}</textarea>
    </div>
    
    <div class="mb-6">
        <label class="flex items-center">
            <input type="checkbox" name="is_active" {% if feature.is_active %}checked{% endif %} 
                   class="mr-2">
            <span class="text-gray-700">Active</span>
        </label>
    </div>
    
    <div class="flex gap-4">
        <button type="submit" class="bg-navy-900 hover:bg-navy-800 text-white px-6 py-3 rounded-lg transition-colors">
            <i class="fas fa-save mr-2"></i>Save Changes
        </button>
        <a href="{% url 'dashboard:index' %}" class="bg-gray-300 hover:bg-gray-400 text-gray-800 px-6 py-3 rounded-lg transition-colors">
            Cancel
        </a>
    </div>
</form>
{% endblock %}
```

#### Template for List View

Create `your_items_list.html`:

```html
{% extends "dashboard/base.html" %}

{% block title %}Your Items{% endblock %}

{% block content %}
<div class="mb-8 flex justify-between items-center">
    <div>
        <h1 class="text-3xl font-bold text-navy-900 mb-2">Your Items</h1>
        <p class="text-gray-600">Manage your items</p>
    </div>
    <a href="{% url 'dashboard:your_item_new' %}" class="bg-navy-900 hover:bg-navy-800 text-white px-6 py-3 rounded-lg transition-colors">
        <i class="fas fa-plus mr-2"></i>Add New Item
    </a>
</div>

<div class="bg-white rounded-lg shadow overflow-hidden">
    <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            {% for item in items %}
            <tr>
                <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900">{{ item.title }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    {% if item.is_active %}
                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">Active</span>
                    {% else %}
                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">Inactive</span>
                    {% endif %}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.sort_order }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <a href="{% url 'dashboard:your_item_edit' item.id %}" class="text-navy-600 hover:text-navy-900 mr-4">
                        <i class="fas fa-edit"></i> Edit
                    </a>
                    <form method="post" class="inline" onsubmit="return confirm('Are you sure you want to delete this item?');">
                        {% csrf_token %}
                        <input type="hidden" name="delete_id" value="{{ item.id }}">
                        <button type="submit" class="text-red-600 hover:text-red-900">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </form>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4" class="px-6 py-4 text-center text-gray-500">No items found. <a href="{% url 'dashboard:your_item_new' %}" class="text-navy-600 hover:underline">Create one</a></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

#### Template for Edit/Create Item

Create `your_item_edit.html`:

```html
{% extends "dashboard/base.html" %}

{% block title %}{% if item.id %}Edit{% else %}Create{% endif %} Item{% endblock %}

{% block content %}
<div class="mb-8">
    <h1 class="text-3xl font-bold text-navy-900 mb-2">
        {% if item.id %}Edit Item{% else %}Create New Item{% endif %}
    </h1>
    <p class="text-gray-600">{% if item.id %}Update item details{% else %}Add a new item{% endif %}</p>
</div>

<form method="post" class="bg-white rounded-lg shadow p-6">
    {% csrf_token %}
    
    <div class="mb-6">
        <label class="block text-gray-700 font-medium mb-2">Title *</label>
        <input type="text" name="title" value="{{ item.title|default:'' }}" 
               class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-navy-500" required>
    </div>
    
    <div class="mb-6">
        <label class="block text-gray-700 font-medium mb-2">Description</label>
        <textarea name="description" rows="5" 
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-navy-500">{{ item.description|default:'' }}</textarea>
    </div>
    
    <div class="mb-6">
        <label class="block text-gray-700 font-medium mb-2">Sort Order</label>
        <input type="number" name="sort_order" value="{{ item.sort_order|default:0 }}" 
               class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-navy-500">
    </div>
    
    <div class="mb-6">
        <label class="flex items-center">
            <input type="checkbox" name="is_active" {% if item.is_active or not item.id %}checked{% endif %} 
                   class="mr-2">
            <span class="text-gray-700">Active</span>
        </label>
    </div>
    
    <div class="flex gap-4">
        <button type="submit" class="bg-navy-900 hover:bg-navy-800 text-white px-6 py-3 rounded-lg transition-colors">
            <i class="fas fa-save mr-2"></i>Save
        </button>
        <a href="{% url 'dashboard:your_items_list' %}" class="bg-gray-300 hover:bg-gray-400 text-gray-800 px-6 py-3 rounded-lg transition-colors">
            Cancel
        </a>
    </div>
</form>
{% endblock %}
```

---

### Step 5: Add to Sidebar Navigation

Edit `myApp/templates/dashboard/base.html` to add a link in the sidebar:

```html
<a href="{% url 'dashboard:your_feature_edit' %}" class="flex items-center px-4 py-3 mb-2 rounded-lg hover:bg-navy-800 transition-colors {% if 'your_feature' in request.resolver_match.url_name %}bg-navy-800{% endif %}">
    <i class="fas fa-icon-name mr-3"></i> Your Feature
</a>
```

**Icon Reference:** Use Font Awesome icons. Common icons:
- `fa-file-alt` - Documents
- `fa-blog` - Blog
- `fa-newspaper` - News
- `fa-calendar` - Events
- `fa-book` - Resources
- `fa-tag` - Tags/Categories

---

## Example: Adding a "Blog Posts" Feature

Let's walk through adding a complete blog posts feature:

### 1. Model (`models.py`)

```python
class BlogPost(models.Model):
    """Blog posts"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    featured_image_url = models.URLField(max_length=500, blank=True)
    author = models.CharField(max_length=200, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
```

### 2. Views (`dashboard_views.py`)

```python
@login_required
def blog_posts_list(request):
    """List all blog posts"""
    posts = BlogPost.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            post_id = request.POST.get('delete_id')
            post = get_object_or_404(BlogPost, id=post_id)
            post.delete()
            messages.success(request, 'Blog post deleted!')
            return redirect('dashboard:blog_posts_list')
    
    context = {'posts': posts}
    return render(request, 'dashboard/blog_posts_list.html', context)


@login_required
def blog_post_edit(request, post_id=None):
    """Edit or create a blog post"""
    if post_id:
        post = get_object_or_404(BlogPost, id=post_id)
    else:
        post = BlogPost()
    
    if request.method == 'POST':
        post.title = request.POST.get('title', '')
        post.content = request.POST.get('content', '')
        post.excerpt = request.POST.get('excerpt', '')
        post.featured_image_url = request.POST.get('featured_image_url', '')
        post.author = request.POST.get('author', '')
        post.is_published = request.POST.get('is_published') == 'on'
        post.sort_order = int(request.POST.get('sort_order', 0))
        
        # Handle published_date
        published_date_str = request.POST.get('published_date', '')
        if published_date_str:
            try:
                from django.utils.dateparse import parse_datetime
                post.published_date = parse_datetime(published_date_str)
            except:
                pass
        
        post.save()
        messages.success(request, 'Blog post saved!')
        return redirect('dashboard:blog_posts_list')
    
    context = {'post': post}
    return render(request, 'dashboard/blog_post_edit.html', context)
```

### 3. URLs (`dashboard_urls.py`)

```python
# Blog Posts
path('blog-posts/', dashboard_views.blog_posts_list, name='blog_posts_list'),
path('blog-posts/new/', dashboard_views.blog_post_edit, name='blog_post_new'),
path('blog-posts/<int:post_id>/', dashboard_views.blog_post_edit, name='blog_post_edit'),
```

### 4. Templates

Create `blog_posts_list.html` and `blog_post_edit.html` following the patterns above.

### 5. Sidebar

Add to `base.html`:
```html
<a href="{% url 'dashboard:blog_posts_list' %}" class="flex items-center px-4 py-3 mb-2 rounded-lg hover:bg-navy-800 transition-colors {% if 'blog' in request.resolver_match.url_name %}bg-navy-800{% endif %}">
    <i class="fas fa-blog mr-3"></i> Blog Posts
</a>
```

---

## Common Patterns

### Pattern 1: Single Instance (Settings-like)
- **Examples:** SEO, Hero, About, Footer
- **Model:** Uses `get_or_create(pk=1)`
- **Views:** One edit view
- **URLs:** One route
- **Templates:** One edit template

### Pattern 2: Multiple Items (CRUD)
- **Examples:** Services, Testimonials, FAQs, Blog Posts
- **Model:** Multiple instances with `sort_order`
- **Views:** List view + Edit/Create view
- **URLs:** List route + New route + Edit route (with ID)
- **Templates:** List template + Edit template

### Pattern 3: Section + Items
- **Examples:** Services Section + Services, FAQ Section + FAQs
- **Model:** One section model + One items model
- **Views:** Section edit view + Items list/edit views
- **URLs:** Section route + Items routes
- **Templates:** Section template + Items templates

---

## Best Practices

### 1. Security
- Always use `@login_required` decorator on dashboard views
- Use `{% csrf_token %}` in all forms
- Validate and sanitize user input
- Use `get_object_or_404()` to prevent errors

### 2. User Experience
- Show success/error messages using Django's messages framework
- Provide clear navigation (breadcrumbs, back buttons)
- Use consistent styling (follow existing patterns)
- Add confirmation dialogs for destructive actions (delete)

### 3. Code Organization
- Keep views focused and single-purpose
- Use descriptive function and variable names
- Add docstrings to functions
- Group related views together in the file

### 4. Database
- Use appropriate field types
- Add indexes for frequently queried fields
- Use `ordering` in Meta class for consistent sorting
- Consider adding `created_at` and `updated_at` timestamps

### 5. Templates
- Extend `base.html` for consistent layout
- Use Tailwind CSS classes (already configured)
- Make forms responsive
- Include helpful placeholder text and labels

### 6. Testing Checklist
After adding a new feature:
- [ ] Create migration and apply it
- [ ] Test creating a new item (if applicable)
- [ ] Test editing an existing item
- [ ] Test deleting an item (if applicable)
- [ ] Test form validation
- [ ] Test navigation links
- [ ] Verify sidebar link works
- [ ] Check responsive design on mobile

---

## Quick Reference

### Required Imports for Views

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
import json
from .models import YourModel
```

### Common Form Fields

```html
<!-- Text Input -->
<input type="text" name="field_name" value="{{ object.field_name|default:'' }}" 
       class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-navy-500">

<!-- Textarea -->
<textarea name="field_name" rows="5" 
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-navy-500">{{ object.field_name|default:'' }}</textarea>

<!-- Checkbox -->
<input type="checkbox" name="is_active" {% if object.is_active %}checked{% endif %}>

<!-- Select Dropdown -->
<select name="field_name" class="w-full px-4 py-2 border border-gray-300 rounded-lg">
    <option value="option1">Option 1</option>
    <option value="option2">Option 2</option>
</select>

<!-- URL Input -->
<input type="url" name="image_url" value="{{ object.image_url|default:'' }}" 
       class="w-full px-4 py-2 border border-gray-300 rounded-lg">
```

### Common View Patterns

```python
# Get or create single instance
obj, created = Model.objects.get_or_create(pk=1)

# Get object or 404
obj = get_object_or_404(Model, id=id)

# Handle POST data
value = request.POST.get('field_name', 'default_value')
is_active = request.POST.get('is_active') == 'on'  # Checkbox
number = int(request.POST.get('number', 0))  # Integer

# Success message
messages.success(request, 'Operation successful!')

# Redirect
return redirect('dashboard:view_name')
```

---

## Troubleshooting

### Issue: Migration errors
**Solution:** Make sure you've imported the model correctly and run `makemigrations` before `migrate`

### Issue: Template not found
**Solution:** Check that the template path matches exactly: `templates/dashboard/your_template.html`

### Issue: URL not working
**Solution:** 
- Verify the URL pattern in `dashboard_urls.py`
- Check that the view function name matches
- Ensure the URL is included in the main `urls.py` (it should be via `include`)

### Issue: Permission denied
**Solution:** Make sure you're logged in and the view has `@login_required` decorator

### Issue: Form not saving
**Solution:**
- Check that `method="post"` is in the form tag
- Verify `{% csrf_token %}` is included
- Check that field names match between template and view

---

## Summary

Adding a new dashboard feature follows this pattern:

1. **Model** → Define database structure
2. **Migration** → Create and apply database changes
3. **Views** → Add view functions for list/edit/create
4. **URLs** → Add URL routes
5. **Templates** → Create HTML forms and lists
6. **Navigation** → Add sidebar link

Follow the existing patterns in the codebase, and your new feature will integrate seamlessly with the dashboard!

---

*Last Updated: 2025*



