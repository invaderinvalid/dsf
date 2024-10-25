from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TrendAnalysis, TrendSuggestion
from .forms import TrendAnalysisForm
from .utils import get_channel_info, generate_trend_suggestions
from django.conf import settings
from .api_utils import get_youtube_channel_data
from .ondemand_api import get_trend_analysis, get_trending_topics

@login_required
def trend_analysis_list(request):
    trending_topics_data = get_trending_topics()
    trending_topics = process_trending_topics(trending_topics_data)
    return render(request, 'trend_analysis/trend_analysis_list.html', {'trending_topics': trending_topics})

@login_required
def trend_analysis_detail(request, topic):
    analysis_data = get_trend_analysis(topic)
    processed_data = process_analysis_data(analysis_data)
    return render(request, 'trend_analysis/trend_analysis_detail.html', {'analysis_data': processed_data, 'topic': topic})

@login_required
def create_trend_analysis(request):
    if request.method == 'POST':
        form = TrendAnalysisForm(request.POST)
        if form.is_valid():
            channel_url = form.cleaned_data['youtube_channel_id']
            channel_data = get_youtube_channel_data(channel_url)
            
            if channel_data:
                analysis = TrendAnalysis.objects.create(
                    user=request.user,
                    youtube_channel_id=channel_url,
                    channel_title=channel_data['title'],
                    channel_description=channel_data['description'],
                    subscriber_count=channel_data['subscriber_count'],
                    view_count=channel_data['view_count'],
                    video_count=channel_data['video_count']
                )
                messages.success(request, 'Trend analysis created successfully.')
                return redirect('trend_analysis_detail', analysis_id=analysis.id)
            else:
                messages.error(request, 'Unable to fetch channel information. Please check the channel URL.')
    else:
        form = TrendAnalysisForm()
    
    return render(request, 'trend_analysis/create_trend_analysis.html', {'form': form})

@login_required
def chat_with_bot(request, suggestion_id):
    suggestion = get_object_or_404(TrendSuggestion, id=suggestion_id)
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        # Implement chat logic here
        bot_response = "This is a placeholder response. Implement actual AI chat here."
        return render(request, 'trend_analysis/chat_with_bot.html', {
            'suggestion': suggestion,
            'bot_response': bot_response
        })
    return render(request, 'trend_analysis/chat_with_bot.html', {'suggestion': suggestion})

def process_trending_topics(data):
    # Process the raw data from on-demand.io to extract trending topics
    # This function should be implemented based on the structure of the response
    # For now, we'll return a placeholder list
    return ["Topic 1", "Topic 2", "Topic 3"]

def process_analysis_data(data):
    # Process the raw data from on-demand.io to extract relevant trend analysis information
    # This function should be implemented based on the structure of the response
    # For now, we'll return a placeholder dictionary
    return {
        "popularity_score": 85,
        "related_keywords": ["keyword1", "keyword2", "keyword3"],
        "sentiment": {
            "positive": 60,
            "neutral": 30,
            "negative": 10
        }
    }
