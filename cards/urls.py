from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('', views.list_cards, name='list_cards'),
    path('create/', views.create_card, name='create_card'),
    path('edit/<int:pk>/', views.edit_card, name='edit_card'),
    path('delete/<int:pk>/', views.delete_card, name='delete_card'),
    path('download/qr/<slug:slug>/', views.download_qr, name='download_qr'),
    path('<slug:slug>/', views.card_detail, name='card_detail'),            # /card/slug/
    path('user/<str:username>/', views.card_by_username, name='card_by_user'),  # /card/user/username/
    path('download/pdf/<slug:slug>/', views.card_pdf, name='card_pdf'),

]
