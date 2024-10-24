from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TrendAnalysis, TrendSuggestion
from .forms import TrendAnalysisForm
from .utils import get_channel_info, generate_trend_suggestions
from django.conf import settings
from .api_utils import get_youtube_channel_data

@login_required
def trend_analysis_list(request):
    analyses = TrendAnalysis.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'trend_analysis/trend_analysis_list.html', {'analyses': analyses})

@login_required
def trend_analysis_detail(request, analysis_id):
    analysis = get_object_or_404(TrendAnalysis, id=analysis_id, user=request.user)
    suggestions = TrendSuggestion.objects.filter(trend_analysis=analysis)
    return render(request, 'trend_analysis/trend_analysis_detail.html', {
        'analysis': analysis,
        'suggestions': suggestions
    })

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
