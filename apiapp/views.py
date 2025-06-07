# apiapp/views.py
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response

# The path to the CSV file *inside the Docker container*
CSV_FILE_PATH = './predicted_topics.csv'

# Load the entire CSV into memory once when the app starts.
try:
    df = pd.read_csv(CSV_FILE_PATH)
    # Add a simple integer index if one doesn't exist to use as an 'id'
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'id'}, inplace=True)
except FileNotFoundError:
    print(f"FATAL ERROR: The data file could not be found at {CSV_FILE_PATH}")
    df = pd.DataFrame()  # Create an empty DataFrame if the file is missing


class AllItemsView(APIView):
    """Returns all records from the CSV."""

    def get(self, request):
        if df.empty:
            return Response({"error": "Data file not found or is empty."}, status=500)
        return Response(df.to_dict('records'))


class ItemDetailView(APIView):
    """Returns a specific item by its id."""

    def get(self, request, item_id):
        if df.empty:
            return Response({"error": "Data file not found or is empty."}, status=500)

        # Look for the item by the 'id' column
        item = df[df['id'] == item_id]

        if item.empty:
            return Response({"error": "Item not found."}, status=404)
        else:
            # Return the first matching item as a dictionary
            return Response(item.iloc[0].to_dict())


class RandomItemsView(APIView):
    """Returns 10 random records from the CSV."""

    def get(self, request):
        if df.empty:
            return Response({"error": "Data file not found or is empty."}, status=500)

        # Ensure we don't try to sample more items than exist
        sample_count = min(10, len(df))
        random_items = df.sample(n=sample_count)
        return Response(random_items.to_dict('records'))


class GroupedItemsView(APIView):
    """Returns all records where a field matches a value."""

    def get(self, request, group_field, group_value):
        if df.empty:
            return Response({"error": "Data file not found or is empty."}, status=500)

        if group_field not in df.columns:
            return Response({"error": f"Invalid group field: {group_field}"}, status=400)

        # URL-decode the group_value to handle spaces, etc.
        from urllib.parse import unquote
        decoded_value = unquote(group_value)

        grouped_items = df[df[group_field] == decoded_value]
        return Response(grouped_items.to_dict('records'))