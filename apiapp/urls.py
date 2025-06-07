from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.AllItemsView.as_view(), name='all-items'),
    path('items/<int:item_id>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('random/', views.RandomItemsView.as_view(), name='random-items'),
    path('groups/<str:group_field>/<str:group_value>/', views.GroupedItemsView.as_view(), name='grouped-items'),
]