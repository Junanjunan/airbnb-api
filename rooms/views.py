from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET", "POST", "DELETE"])
def list_rooms(request):
    return Response()
