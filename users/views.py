from rooms.models import Room
from users.serializers import ReadUserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rooms.serializers import RoomSerializer
from .serializers import ReadUserSerializer, WriteUserSerializer
from .models import User


class MeView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ReadUserSerializer(request.user).data)

    def put(self, request):
        serializer = WriteUserSerializer(request.user, data=request.data, partial=True)        # request.user: instance임
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(ReadUserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# @api_view(["GET", "POST"])     # database의 state를 바꿔주기 때문에 GET이 아닌 POST 이어야 한다??     # 아래 FavsView 하기 전에 시도되었던 FBV
# @permission_classes([IsAuthenticated])    # 이용해주려면, from rest_framework.decorators import permission_classes 호출
# def toggle_fav(request):
#     room = request.data.get("room")
#     print(room)


class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer)

    def put(self, request):             # favs를 만드는 것이 아니라, 있는 favs를 수정해주는 것이니까 post가 아니라 put method
        pass