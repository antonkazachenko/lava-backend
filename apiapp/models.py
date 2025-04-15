from django.db import models

class TopicItem(models.Model):
    topic = models.CharField(max_length=100)
    website_url = models.URLField()
    cleaned_website_text = models.TextField()

    def __str__(self):
        return f"{self.website_url} ({self.topic})"

    class Meta:
        db_table = 'topics'
        ordering = ['id']