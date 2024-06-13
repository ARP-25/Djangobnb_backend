from django.forms import ModelForm
from property.models import Property

class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = ["name","description","price_per_night", "bedrooms", "bathrooms", "guests", "country", "country_code", "category", "image"]
    