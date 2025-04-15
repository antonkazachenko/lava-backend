from rest_framework import serializers
from .models import TopicItem

class TopicItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicItem
        fields = ['id', 'topic', 'website_url', 'cleaned_website_text']

class TopicItemSummarySerializer(serializers.ModelSerializer):
    text_snippet = serializers.SerializerMethodField()

    class Meta:
        model = TopicItem
        fields = ['id', 'website_url', 'topic', 'text_snippet']

    def get_text_snippet(self, obj):
        # Return the first 100 characters of the cleaned text as a snippet
        return obj.cleaned_website_text[:100]
