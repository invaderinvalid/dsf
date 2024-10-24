from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from cryptography.fernet import Fernet

class TrendAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    youtube_channel_id = models.CharField(max_length=255)
    channel_title = models.CharField(max_length=255)
    channel_description = models.TextField(blank=True)
    subscriber_count = models.IntegerField()
    view_count = models.IntegerField()
    video_count = models.IntegerField()
    topics = models.TextField(blank=True)
    trending_keywords = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_youtube_channel_id(self, channel_id):
        f = Fernet(settings.ENCRYPTION_KEY)
        self.youtube_channel_id = f.encrypt(channel_id.encode()).decode()

    def get_youtube_channel_id(self):
        f = Fernet(settings.ENCRYPTION_KEY)
        return f.decrypt(self.youtube_channel_id.encode()).decode()

    def __str__(self):
        return f"Trend Analysis for {self.channel_title}"

class TrendSuggestion(models.Model):
    trend_analysis = models.ForeignKey(TrendAnalysis, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    description = models.TextField()
    video_length = models.IntegerField()  # in seconds
    language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic
