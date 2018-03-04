from rest_framework import serializers
from rest_framework.validators import ValidationError

from api import models


class WorkExperienceValidate(object):
    """自定义验证规则"""

    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if value != self.base:
            raise serializers.ValidationError('你的输入有误，必须是%s' % self.base)


class DrfSerialize(serializers.ModelSerializer):
    class Meta:
        model = models.DegreeRegistrationForm
        # fields = '__all__'
        exclude = ['enrolled_degree']
        # 自定义验证规则
        extra_kwargs = {
            'current_position': {'required': True},
            'current_salary': {'validators': [WorkExperienceValidate(222), ]}
        }

    # 自定义钩子函数进行验证
    def validate_your_expectation(self, valited_value):
        if len(valited_value) < 10:
            raise ValidationError(detail='长度不够，请重新输入')
        return valited_value
