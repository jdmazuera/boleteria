from django.contrib import admin
from django.urls import path,include
from events_manager.receipt.views import AddToShoppingCarView,DetailShoppingCar,DeleteItemShoppingCarView,UpdateItemShoppingCarView,DetailReceiptView

app_name = 'receipt'

urlpatterns = [
    path('add_to_shopping_car', AddToShoppingCarView.as_view(), name='add_to_shopping_car'),
    path('detail_shopping_car', DetailShoppingCar.as_view(), name='detail_shopping_car'),
    path('delete_item_shopping_car', DeleteItemShoppingCarView.as_view(), name='delete_item_shopping_car'),
    path('update_item_shopping_car', UpdateItemShoppingCarView.as_view(), name='update_item_shopping_car'),
    path('<int:pk>', DetailReceiptView.as_view(), name='detail')
]