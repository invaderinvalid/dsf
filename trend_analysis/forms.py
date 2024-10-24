from django import forms
from .models import TrendAnalysis

class TrendAnalysisForm(forms.ModelForm):
    youtube_channel_id = forms.URLField(help_text="Enter the YouTube channel URL")

    class Meta:
        model = TrendAnalysis
        fields = ['youtube_channel_id']

    def clean_youtube_channel_id(self):
        channel_id = self.cleaned_data['youtube_channel_id']
        # You could add validation here to check if it's a valid YouTube channel ID
        return channel_id
