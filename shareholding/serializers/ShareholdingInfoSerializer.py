from rest_framework import serializers

from ..models import ShareholdingInfo

class ShareholdingInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShareholdingInfo
        fields = "__all__"