from rest_framework import serializers
from property.models import Property, Reservation
from useraccount.serializers import UserDetailSerializer

class PropertyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'name', 'price_per_night', 'image_url']

class PropertyDetailSerializer(serializers.ModelSerializer):
    host = UserDetailSerializer(read_only=True, many=False)
    class Meta:
        model = Property
        fields = ['id', 'name', 'price_per_night', 'image_url', 'description', 'price_per_night', 'bedrooms', 'bathrooms', 'guests', 'host']


class ReservationsListSerializer(serializers.ModelSerializer):
    property = PropertyListSerializer(read_only=True, many=False)
    class Meta:
        model = Reservation
        fields = ['id', 'property', 'start_date', 'end_date', 'number_of_nights', 'total_price', 'guests']

        