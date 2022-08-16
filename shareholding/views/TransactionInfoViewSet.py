from datetime import datetime, timezone
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from ..models import ShareholdingInfo
from ..serializers import ShareholdingInfoSerializer

class TransactionInfoViewSet(viewsets.ModelViewSet):
    
    queryset = ShareholdingInfo.objects.all()
    serializer_class = ShareholdingInfoSerializer

    def list(self, request):

        stock = self.request.query_params.get("stock")
        date = self.request.query_params.get("date")
        thresh = abs(float(self.request.query_params.get("thresh")))

        queryset = self.queryset

        date = datetime.strptime(date, "%Y-%m-%d")
        query_set_greater = queryset.filter(stock=stock)\
                        .filter(date=date)\
                        .filter(difference_percentage__gte = thresh)

        query_set_smaller = queryset.filter(stock=stock)\
                        .filter(date=date)\
                        .filter(difference_percentage__lte = -thresh)

        query_set = list(query_set_greater) + list(query_set_smaller)

        if len(query_set) == 0:
            return Response(
                    {'message': 'Change criteria'},
                    status=status.HTTP_204_NO_CONTENT
                )

        serializer = self.serializer_class(query_set, many = True)
        return Response(serializer.data)


    # def get_queryset(self):

    #     stock = self.request.query_params.get("stock")
    #     date = self.request.query_params.get("date")
    #     thresh = abs(float(self.request.query_params.get("thresh")))
    #     queryset = self.queryset

    #     date = datetime.strptime(date, "%Y-%m-%d")
    #     query_set = queryset.filter(stock=stock)\
    #                     .filter(date=date)\
    #                     .filter(difference_percentage__gte = thresh,
    #                             difference_percentage__lte = -thresh)

    #     if query_set.count() == 0:
    #         return Response(
    #                 {'message': 'Change criteria'},
    #                 status=status.HTTP_204_NO_CONTENT
    #             )

    #     return query_set
        
