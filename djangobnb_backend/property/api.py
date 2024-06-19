from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from . forms import PropertyForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from property.models import Property, Reservation
from property.serializers import PropertyListSerializer, ReservationsListSerializer, PropertyDetailSerializer
from useraccount.models import User
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework.permissions import AllowAny



# @api_view(['GET'])
# @authentication_classes([])
# @permission_classes([])
# def property_list(request):
#     #
#     # Auth

#     try:
#         token = request.META['HTTP_AUTHORIZATION'].split('Bearer ')[1]
#         token = AccessToken(token)
#         user_id = token.payload['user_id']
#         user = User.objects.get(pk=user_id)
#     except Exception as e:
#         user = None

#     #
#     #

#     favorites = []
#     properties = Property.objects.all()

#     #
#     # Filter

#     is_favorites = request.GET.get('is_favorites', '')
#     host_id = request.GET.get('host_id', '')

#     country = request.GET.get('country', '')
#     category = request.GET.get('category', '')
#     print('category', category)
#     checkin_date = request.GET.get('checkIn', '')
#     checkout_date = request.GET.get('checkOut', '')
#     bedrooms = request.GET.get('numBedrooms', '')
#     guests = request.GET.get('numGuests', '')
#     bathrooms = request.GET.get('numBathrooms', '')

#     print('country', country)

#     if checkin_date and checkout_date:
#         exact_matches = Reservation.objects.filter(start_date=checkin_date) | Reservation.objects.filter(end_date=checkout_date)
#         overlap_matches = Reservation.objects.filter(start_date__lte=checkout_date, end_date__gte=checkin_date)
#         all_matches = []

#         for reservation in exact_matches | overlap_matches:
#             all_matches.append(reservation.property_id)
        
#         properties = properties.exclude(id__in=all_matches)

#     if host_id:
#         properties = properties.filter(host_id=host_id)

#     if is_favorites:
#         properties = properties.filter(favorited__in=[user])
    
#     if guests:
#         properties = properties.filter(guests__gte=guests)
    
#     if bedrooms:
#         properties = properties.filter(bedrooms__gte=bedrooms)
    
#     if bathrooms:
#         properties = properties.filter(bathrooms__gte=bathrooms)
    
#     if country:
#         properties = properties.filter(country=country)
    
#     if category and category.lower() != 'undefined':
#         properties = properties.filter(category__iexact=category)
    
#     #
#     # Favorites
        
#     if user:
#         for property in properties:
#             if user in property.favorited.all():
#                 favorites.append(property.id)

#     #
#     #

#     serializer = PropertyListSerializer(properties, many=True)

#     return JsonResponse({
#         'data': serializer.data,
#         'favorites': favorites
#     })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def property_list(request):
    # Auth
    user = None
    try:
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        if auth_header:
            token = auth_header.split('Bearer ')[1]
            token = AccessToken(token)
            user_id = token.payload['user_id']
            user = User.objects.get(pk=user_id)
    except Exception as e:
        user = None

    favorites = []
    properties = Property.objects.all()

    # Filter
    is_favorites = request.GET.get('is_favorites', '')
    host_id = request.GET.get('host_id', '')
    country = request.GET.get('country', '')
    category = request.GET.get('category', '')
    checkin_date = request.GET.get('checkIn', '')
    checkout_date = request.GET.get('checkOut', '')
    bedrooms = request.GET.get('numBedrooms', '')
    guests = request.GET.get('numGuests', '')
    bathrooms = request.GET.get('numBathrooms', '')

    if checkin_date and checkout_date:
        exact_matches = Reservation.objects.filter(start_date=checkin_date) | Reservation.objects.filter(end_date=checkout_date)
        overlap_matches = Reservation.objects.filter(start_date__lte=checkout_date, end_date__gte=checkin_date)
        all_matches = [reservation.property_id for reservation in (exact_matches | overlap_matches)]
        properties = properties.exclude(id__in=all_matches)

    if host_id:
        properties = properties.filter(host_id=host_id)

    if is_favorites and user:
        properties = properties.filter(favorited__in=[user])

    if guests:
        properties = properties.filter(guests__gte=guests)

    if bedrooms:
        properties = properties.filter(bedrooms__gte=bedrooms)

    if bathrooms:
        properties = properties.filter(bathrooms__gte=bathrooms)

    if country:
        properties = properties.filter(country=country)

    if category and category.lower() != 'undefined':
        properties = properties.filter(category__iexact=category)

    # Favorites
    if user:
        favorites = [property.id for property in properties if user in property.favorited.all()]

    serializer = PropertyListSerializer(properties, many=True)

    return JsonResponse({
        'data': serializer.data,
        'favorites': favorites
    })


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_detail(request, pk):
    property = Property.objects.get(pk=pk)

    serializer = PropertyDetailSerializer(property, many=False)

    return JsonResponse(serializer.data)



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_property(request):
    form = PropertyForm(request.data, request.FILES)
    if form.is_valid():
        property = form.save(commit=False)
        property.host = request.user
        property.save()
        return JsonResponse({"message": "Property created successfully", "success": True}, status=201)
    else:
        print('error', form.errors, form.non_field_errors)
        return JsonResponse({"errors": form.errors}, status=400)
    


@api_view(['POST'])
def book_property(request, pk):
    try:
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        number_of_nights = request.POST.get('number_of_nights')
        total_price = request.POST.get('total_price')
        guests = request.POST.get('guests')

        property = Property.objects.get(pk=pk)
        Reservation.objects.create(
            property=property,
            start_date=start_date,
            end_date=end_date,
            number_of_nights=number_of_nights,
            total_price=total_price,
            guests=guests,
            created_by=request.user
        )
        return JsonResponse({"message": "Booking successful", "success": True}, status=201)

    except Exception as e:
        return JsonResponse({"message": str(e), "success": False}, status=400)
    

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_reservations(request, pk):
    try:
        property = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return JsonResponse({'error': 'Property not found'}, status=404)
    
    reservations = property.reservations.all()
    serializer = ReservationsListSerializer(reservations, many=True)
    
    return JsonResponse(serializer.data, safe=False, status=200)


@api_view(['POST'])
def toggle_favorite(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.user in property.favorited.all():
        property.favorited.remove(request.user)
        return JsonResponse({'message': 'Property removed from favorites', 'is_favorite': False}, status=200)
    else:
        property.favorited.add(request.user)
        return JsonResponse({'message': 'Property added to favorites', 'is_favorite': True}, status=200)