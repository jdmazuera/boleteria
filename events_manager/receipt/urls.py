from django.contrib import admin
from django.urls import path,include
from events_manager.receipt.views import *

app_name = 'receipt'

urlpatterns = [
    path('add_to_shopping_car', AddToShoppingCarView.as_view(), name='add_to_shopping_car'),
    path('detail_shopping_car', DetailShoppingCar.as_view(), name='detail_shopping_car'),
    path('delete_item_shopping_car', DeleteItemShoppingCarView.as_view(), name='delete_item_shopping_car'),
    path('update_item_shopping_car', UpdateItemShoppingCarView.as_view(), name='update_item_shopping_car'),
    path('', ReceiptListView.as_view(), name='list'),
    path('<int:pk>', DetailReceiptView.as_view(), name='detail'),
    path('create/',ReceiptCreateView.as_view(),name='create'),
    path('update/<int:pk>',ReceiptUpdateView.as_view(),name='update'),
    path('delete/<int:pk>',ReceiptDeleteView.as_view(),name='delete')
    
]