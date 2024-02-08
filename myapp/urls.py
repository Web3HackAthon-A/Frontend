from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('index/', views.index, name='index'),
    path('create_nft/', views.create_nft, name='create_nft'),
    path('view_content/', views.view_content, name='view_content'),
    path('confirm/', views.confirm, name='confirm'),
    path('transaction_receipt/<str:tx_hash>/', views.create_nft, name='transaction*_receipt')
]
