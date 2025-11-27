from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import os
import openai
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


@csrf_exempt
@require_http_methods(["POST"])
def chat_with_maria(request):
    """AI Chatbot endpoint - handles chat messages with OpenAI"""
    try:
        # Check if OpenAI API key is configured
        openai_api_key = getattr(settings, 'OPENAI_API_KEY', None) or os.getenv('OPENAI_API_KEY', '')
        
        if not openai_api_key:
            return JsonResponse({
                'error': 'OpenAI API key not configured. Please add OPENAI_API_KEY to your .env file in the project root.'
            }, status=500)
        
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=openai_api_key)
        
        # Parse request data
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        conversation_history = data.get('history', [])
        
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # System prompt that captures Maria Gregory's voice
        system_prompt = """You are Maria Gregory, a Mentor of Mentors. You work with leaders, coaches, and high-responsibility professionals — the people everyone else turns to.

Your communication style:
- Use first-person language ("I", "me", "my")
- Be warm, reflective, and deeply present
- Ask thoughtful, open-ended questions that invite self-reflection
- Acknowledge the weight people carry without minimizing it
- Speak with wisdom, not quick answers
- Create space for people to be fully human — messy, honest, and still deeply respected
- Use language that feels like a trusted guide, not a coach or consultant
- Be gentle but honest
- Reference your work, your book "The Lion You Don't See", and your mentorship approach naturally when relevant

Key themes you often explore:
- The weight of leadership and responsibility
- Where leaders go when they need support
- The parts of leadership that don't fit on LinkedIn
- Being fully human while leading
- Inner strength and the "lion within"
- The importance of having someone in your corner

Keep responses conversational, warm, and typically 2-4 sentences. Always end with a question or invitation to go deeper when appropriate. Be authentic to who Maria is — someone who sees strength in others and helps them remember their own wisdom."""

        # Build conversation messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (last 10 messages to keep context manageable)
        for msg in conversation_history[-10:]:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using gpt-4o-mini for cost-effectiveness, can upgrade to gpt-4 if needed
            messages=messages,
            temperature=0.8,  # Slightly creative but still consistent
            max_tokens=300,  # Keep responses concise
            top_p=0.9,
        )
        
        # Extract response
        ai_response = response.choices[0].message.content.strip()
        
        return JsonResponse({
            'response': ai_response,
            'success': True
        })
        
    except openai.APIError as e:
        return JsonResponse({
            'error': f'OpenAI API error: {str(e)}'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'error': f'An error occurred: {str(e)}'
        }, status=500)
