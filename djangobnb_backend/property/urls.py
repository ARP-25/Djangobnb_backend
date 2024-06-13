from django.urls import path

from . import api

urlpatterns = [
    path('', api.property_list),
    path('create/', api.create_property),
    path('<uuid:pk>/', api.property_detail),
    path('<uuid:pk>/book/', api.book_property),
    path('<uuid:pk>/reservations/', api.property_reservations),
    path('<uuid:pk>/toggle_favorite/', api.toggle_favorite),
]