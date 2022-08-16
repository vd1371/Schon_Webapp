from datetime import datetime, timezone
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from ..models import ShareholdingInfo
from ..serializers import ShareholdingInfoSerializer

class ShareholdingInfoViewSet(viewsets.ModelViewSet):
    
    queryset = ShareholdingInfo.objects.all()
    serializer_class = ShareholdingInfoSerializer

    def get_queryset(self):

        stock = self.request.query_params.get("stock")
        date = self.request.query_params.get("date")
        queryset = self.queryset

        if stock:
            date = datetime.strptime(date, "%Y-%m-%d")
            query_set = queryset.filter(stock=stock).filter(date=date)
        
        elif date:
            date = datetime.strptime(date, "%Y-%m-%d")
            query_set = queryset.filter(date=date)

        elif stock and date:
            date = datetime.strptime(date, "%Y-%m-%d")
            query_set = queryset.filter(stock=stock).filter(date=date)

        return query_set
        
