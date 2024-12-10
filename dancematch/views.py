from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Dancer
from .permissions import AllowPostWithoutAuthentication
from .serializers import DancerSerializer


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}, you are authenticated!"})


class DancerViewSet(ModelViewSet):
    
    serializer_class = DancerSerializer
    queryset = Dancer.objects.all()
    permission_classes = [AllowPostWithoutAuthentication]
    
    def perform_destroy(self, instance):
        instance.user.delete()
        instance.delete()
