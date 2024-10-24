import google.generativeai as genai
from .api_utils import get_youtube_channel_data, get_google_trends_data, get_video_performance
import openai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
openai.api_key = settings.OPENAI_API_KEY

def get_channel_info(channel_id):
    return get_youtube_channel_data(channel_id)

def generate_trend_suggestions(analysis):
    channel_title = analysis.channel_title
    trending_keywords = analysis.trending_keywords.split(', ')
    
    prompt = f"Generate 5 video topic suggestions for a YouTube channel titled '{channel_title}' based on these trending keywords: {', '.join(trending_keywords)}. For each suggestion, include a title, brief description, estimated video length in seconds, and target language."
    
    if settings.USE_GEMINI:
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            suggestions_text = response.text
        except Exception as e:
            print(f"Error using Gemini: {e}. Falling back to OpenAI.")
            suggestions_text = generate_openai_suggestions(prompt)
    else:
        suggestions_text = generate_openai_suggestions(prompt)

    suggestions_list = suggestions_text.split('\n\n')
    
    suggestions = []
    for suggestion in suggestions_list:
        lines = suggestion.split('\n')
        if len(lines) >= 4:
            suggestions.append({
                'topic': lines[0].strip(),
                'description': lines[1].strip(),
                'video_length': int(lines[2].split(':')[1].strip()),
                'language': lines[3].split(':')[1].strip()
            })
    
    return suggestions

def generate_openai_suggestions(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()
