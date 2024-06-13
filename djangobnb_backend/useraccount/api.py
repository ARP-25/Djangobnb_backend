from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404
from useraccount.serializers import UserDetailSerializer
from useraccount.models import User
from property.serializers import ReservationsListSerializer
from property.models import Property

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def host_detail(request, pk):
    print("PK ======================>", pk)
    user = get_object_or_404(User, pk=pk)
    print("User Avatar URL ======================>", user.avatar_url)
    # print("User  Name ======================>", user.name)
    serializer = UserDetailSerializer(user, many=False)

    return JsonResponse(serializer.data, safe=False, status=200)


@api_view(['GET'])
def reservations_list(request):
    reservations = request.user.reservations.all()
    print("User ==========================>", request.user)
    serializer = ReservationsListSerializer(reservations, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)


