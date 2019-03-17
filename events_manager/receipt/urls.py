from django.contrib import admin
from django.urls import path,include
from events_manager.receipt.views import AddToShoppingCarView,DetailShoppingCar,UpdateShoppingCarView

app_name = 'receipt'

urlpatterns = [
    path('add_to_shopping_car', AddToShoppingCarView.as_view(), name='add_to_shopping_car'),
    path('detail_shopping_car', DetailShoppingCar.as_view(), name='detail_shopping_car'),
    path('update_shopping_car', UpdateShoppingCarView.as_view(), name='update_shopping_car')
]