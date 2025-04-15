from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import TopicItem
from .serializers import TopicItemSerializer, TopicItemSummarySerializer
import random

# 1. Fetch Items by Group
class GroupedItemsView(APIView):
    """
    GET /api/groups/{group_field}/{group_value}/?page=1&pageSize=50
    Returns all records where the specified group field matches group_value.
    Allowed group fields: 'topic', 'website_url', 'cleaned_website_text'
    """
    allowed_fields = ['topic', 'website_url', 'cleaned_website_text']

    def get(self, request, group_field, group_value):
        if group_field not in self.allowed_fields:
            return Response(
                {"error": f"Invalid group field. Allowed fields: {', '.join(self.allowed_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        queryset = TopicItem.objects.filter(**{group_field: group_value})
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 50)
        paginator = Paginator(queryset, page_size)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = []
        serializer = TopicItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 2. Fetch a Specific Item (Detailed View)
class ItemDetailView(generics.RetrieveAPIView):
    """
    GET /api/items/{id}/
    Returns all details for the item with the given id.
    """
    queryset = TopicItem.objects.all()
    serializer_class = TopicItemSerializer
    lookup_field = 'id'

# 3. Fetch 10 Random Items (Summary View)
class RandomItemsView(APIView):
    """
    GET /api/random/
    Returns a summary view of 10 random records.
    """
    def get(self, request):
        count = 10
        all_ids = list(TopicItem.objects.values_list('id', flat=True))
        if not all_ids:
            return Response([], status=status.HTTP_200_OK)
        random_ids = random.sample(all_ids, min(count, len(all_ids)))
        queryset = TopicItem.objects.filter(id__in=random_ids)
        serializer = TopicItemSummarySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 4. Fetch All Items with Pagination
class AllItemsView(APIView):
    """
    GET /api/items/?page=1&pageSize=50
    Returns all records with pagination.
    """
    def get(self, request):
        queryset = TopicItem.objects.all()
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 50)
        paginator = Paginator(queryset, page_size)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = []
        serializer = TopicItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
