# apiapp/management/commands/populate_db.py
import pandas as pd
from django.core.management.base import BaseCommand
from apiapp.models import TopicItem

class Command(BaseCommand):
    help = 'Loads pre-processed data from predicted_topics.csv.'
    def handle(self, *args, **options):
        self.stdout.write("Loading data from predicted_topics.csv...")
        df = pd.read_csv('./predicted_topics.csv')
        TopicItem.objects.all().delete()
        items_to_create = [
            TopicItem(
                website_url=row['website_url'],
                cleaned_website_text=row['cleaned_website_text'],
                topic=row['Predicted_Label']
            ) for index, row in df.iterrows()
        ]
        TopicItem.objects.bulk_create(items_to_create)
        self.stdout.write(self.style.SUCCESS("Successfully loaded records."))