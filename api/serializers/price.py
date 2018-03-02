from rest_framework import serializers
from .. import models


class PricePolicyModelSerializer(serializers.ModelSerializer):
    valid_period = serializers.SerializerMethodField()

    class Meta:
        model = models.PricePolicy
        fields = '__all__'
        depth = 2

    def get_valid_period(self, obj):
        return obj.get_valid_period_display()


