from rest_framework import viewsets

from ..models import ShareholdingInfo
from ..serializers import ShareholdingInfoSerializer

class ShareholdingInfoViewSet(viewsets.ModelViewSet):
    
    queryset = ShareholdingInfo.objects.all()
    serializer_class = ShareholdingInfoSerializer